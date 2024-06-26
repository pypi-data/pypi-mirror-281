import inspect
import json
import opcode
import os
import sys
import re
import collections
import itertools
import threading
import traceback
from typing import Any, Set


def objjson(obj: Any) -> Any:
    return _objjson(obj, set())


def _objjson(obj: Any, memo: Set[int]) -> Any:
    """
    return a jsonifiable object from obj
    """
    if isinstance(obj, (str, int, float)) or obj is None:
        return obj

    if id(obj) in memo:
        raise ValueError("Can't jsonify a recursive object")

    memo.add(id(obj))

    if isinstance(obj, (list, tuple)):
        return [_objjson(elem, memo.copy()) for elem in obj]

    if isinstance(obj, dict):
        return {key: _objjson(val, memo.copy()) for key, val in obj.items()}

    # For generic object
    ret = {"__class__": type(obj).__name__}

    if hasattr(obj, "__dict__"):
        for key, val in obj.__dict__.items():
            ret[key] = _objjson(val, memo.copy())

    return ret


file_reading_errors = (
    IOError,
    OSError,
    ValueError # IronPython weirdness.
)


def get_repr_function(item, custom_repr):
    for condition, action in custom_repr:
        if isinstance(condition, type):
            condition = lambda x, y=condition: isinstance(x, y)
        if condition(item):
            return action
    return repr


DEFAULT_REPR_RE = re.compile(r' at 0x[a-f0-9A-F]{4,}')


def get_shortish_repr(item, custom_repr=(), max_length=None, normalize=False):
    repr_function = get_repr_function(item, custom_repr)
    try:
        r = repr_function(item)
    except Exception:
        r = 'REPR FAILED'
    r = r.replace('\r', '').replace('\n', '')
    # if normalize:
    #     r = normalize_repr(r)
    if max_length:
        r = truncate(r, max_length)
    return r


def truncate(string, max_length):
    if (max_length is None) or (len(string) <= max_length):
        return string
    else:
        left = (max_length - 3) // 2
        right = max_length - 3 - left
        return u'{}...{}'.format(string[:left], string[-right:])


def ensure_tuple(x):
    if isinstance(x, inspect.collections_abc.Iterable) and \
                                               not isinstance(x, (str,)):
        return tuple(x)
    else:
        return (x,)


ipython_filename_pattern = re.compile('^<ipython-input-([0-9]+)-.*>$')
ansible_filename_pattern = re.compile(r'^(.+\.zip)[/|\\](ansible[/|\\]modules[/|\\].+\.py)$')
RETURN_OPCODES = {
    'RETURN_GENERATOR', 'RETURN_VALUE', 'RETURN_CONST',
    'INSTRUMENTED_RETURN_GENERATOR', 'INSTRUMENTED_RETURN_VALUE',
    'INSTRUMENTED_RETURN_CONST', 'YIELD_VALUE', 'INSTRUMENTED_YIELD_VALUE'
}


def get_local_reprs(frame, watch=(), custom_repr=(), max_length=None, normalize=False):
    code = frame.f_code
    vars_order = (code.co_varnames + code.co_cellvars + code.co_freevars +
                  tuple(frame.f_locals.keys()))

    result_items = [(key, get_shortish_repr(value, custom_repr,
                                                  max_length, normalize))
                    for key, value in frame.f_locals.items()]
    result_items.sort(key=lambda key_value: vars_order.index(key_value[0]))
    result = collections.OrderedDict(result_items)

    for variable in watch:
        result.update(sorted(variable.items(frame, normalize)))
    return result


class UnavailableSource(object):
    def __getitem__(self, i):
        return u'SOURCE IS UNAVAILABLE'


source_and_path_cache = {}


def get_path_and_source_from_frame(frame):
    globs = frame.f_globals or {}
    module_name = globs.get('__name__')
    file_name = frame.f_code.co_filename
    cache_key = (module_name, file_name)
    try:
        return source_and_path_cache[cache_key]
    except KeyError:
        pass
    loader = globs.get('__loader__')

    source = None
    if hasattr(loader, 'get_source'):
        try:
            source = loader.get_source(module_name)
        except ImportError:
            pass
        if source is not None:
            source = source.splitlines()
    if source is None:
        ipython_filename_match = ipython_filename_pattern.match(file_name)
        ansible_filename_match = ansible_filename_pattern.match(file_name)
        if ipython_filename_match:
            entry_number = int(ipython_filename_match.group(1))
            try:
                import IPython
                ipython_shell = IPython.get_ipython()
                ((_, _, source_chunk),) = ipython_shell.history_manager. \
                                  get_range(0, entry_number, entry_number + 1)
                source = source_chunk.splitlines()
            except Exception:
                pass
        elif ansible_filename_match:
            try:
                import zipfile
                archive_file = zipfile.ZipFile(ansible_filename_match.group(1), 'r')
                source = archive_file.read(ansible_filename_match.group(2).replace('\\', '/')).splitlines()
            except Exception:
                pass
        else:
            try:
                with open(file_name, 'rb') as fp:
                    source = fp.read().splitlines()
            except file_reading_errors:
                pass
    if not source:
        source = UnavailableSource()

    if isinstance(source[0], bytes):
        encoding = 'utf-8'
        for line in source[:2]:
            match = re.search(br'coding[:=]\s*([-\w.]+)', line)
            if match:
                encoding = match.group(1).decode('ascii')
                break
        source = [str(sline, encoding, 'replace') for sline in
                  source]

    result = (file_name, source)
    source_and_path_cache[cache_key] = result
    return result


def get_write_function(output, overwrite):
    is_path = isinstance(output, (os.PathLike, str))
    if overwrite and not is_path:
        raise Exception('`overwrite=True` can only be used when writing '
                        'content to file.')
    if output is None:
        def write(s):
            # output nothing by default
            pass
            # stderr = sys.stderr
            # try:
            #     stderr.write(s)
            # except UnicodeEncodeError:
            #     # God damn Python 2
            #     stderr.write(shitcode(s))
    elif is_path:
        return FileWriter(output, overwrite).write
    elif callable(output):
        write = output
    else:
        def write(s):
            output.write(s)
    return write


class FileWriter(object):
    def __init__(self, path, overwrite):
        self.path = str(path)
        self.overwrite = overwrite

    def write(self, s):
        with open(self.path, 'w' if self.overwrite else 'a',
                  encoding='utf-8') as output_file:
            output_file.write(s)
        self.overwrite = False


thread_global = threading.local()
DISABLED = bool(os.getenv('PYSNOOPER_DISABLED', ''))


def var_filter(var):
    var_value = repr(var)
    if not var_value.startswith('<'):
        return False
    if var_value.startswith('<function') or var_value.startswith('<class') or var_value.startswith('<module'):
        return False
    return True


def obj_var_printer(var):
    return json.dumps(objjson(var))


class FuncCallTracer:
    def __init__(self, output=None, depth=10,
                 prefix='', overwrite=False, thread_info=False,
                 max_variable_length=2000, normalize=False, relative_time=False,
                 source_set=None, summary_on_exit=True):
        self._write = get_write_function(output, overwrite)
        self.source_set = source_set
        self.accept_files = set()
        self.summary_on_exit = summary_on_exit

        self.watch = []
        self.frame_to_local_reprs = {}
        self.depth = depth
        self.prefix = prefix
        self.thread_info = thread_info
        self.thread_info_padding = 0
        assert self.depth >= 1
        self.target_codes = set()
        self.target_frames = set()
        self.thread_local = threading.local()
        self.custom_repr = ((var_filter, obj_var_printer),)
        self.last_source_path = None
        self.max_variable_length = max_variable_length
        self.normalize = normalize
        self.relative_time = relative_time
        # LOGGER
        self.var_logger = {}
        self.cur_source_file = None
        self.call_var_list = {}
        self.cur_func = None

    def write(self, s):
        s = u'{self.prefix}{s}\n'.format(**locals())
        self._write(s)

    def __enter__(self):
        if DISABLED:
            return
        thread_global.__dict__.setdefault('depth', -1)
        calling_frame = inspect.currentframe().f_back
        if not self._is_internal_frame(calling_frame):
            calling_frame.f_trace = self.trace
            self.target_frames.add(calling_frame)

        stack = self.thread_local.__dict__.setdefault(
            'original_trace_functions', []
        )
        stack.append(sys.gettrace())
        # self.start_times[calling_frame] = datetime_module.datetime.now()
        sys.settrace(self.trace)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if DISABLED:
            return
        stack = self.thread_local.original_trace_functions
        sys.settrace(stack.pop())
        calling_frame = inspect.currentframe().f_back
        self.target_frames.discard(calling_frame)
        self.frame_to_local_reprs.pop(calling_frame, None)

        if self.summary_on_exit:
            print(f'FUNC CALL INFO:{json.dumps(self.var_logger, ensure_ascii=False)}')

    def _is_internal_frame(self, frame):
        return frame.f_code.co_filename == FuncCallTracer.__enter__.__code__.co_filename

    def set_thread_info_padding(self, thread_info):
        current_thread_len = len(thread_info)
        self.thread_info_padding = max(self.thread_info_padding,
                                       current_thread_len)
        return thread_info.ljust(self.thread_info_padding)

    def trace(self, frame, event, arg):
        if not (frame.f_code in self.target_codes or frame in self.target_frames):
            if self.depth == 1:
                return None
            elif self._is_internal_frame(frame):
                return None
            else:
                _frame_candidate = frame
                for i in range(1, self.depth):
                    _frame_candidate = _frame_candidate.f_back
                    if _frame_candidate is None:
                        return None
                    elif _frame_candidate.f_code in self.target_codes or _frame_candidate in self.target_frames:
                        break
                else:
                    return None

        if event == 'call':
            thread_global.depth += 1
        indent = ' ' * 4 * thread_global.depth

        line_no = frame.f_lineno
        source_path, source = get_path_and_source_from_frame(frame)
        source_path = source_path if not self.normalize else os.path.basename(source_path)
        print_in_this_file = False
        if self.source_set is not None:
            if source_path in self.accept_files:
                print_in_this_file = True
            else:
                for accpet_prefix in self.source_set:
                    if source_path.startswith(accpet_prefix):
                        print_in_this_file = True
                        self.accept_files.add(source_path)
                        break
        else:
            print_in_this_file = True

        if self.last_source_path != source_path:
            if print_in_this_file:
                self.cur_source_file = source_path
                if self.cur_source_file not in self.var_logger:
                    self.var_logger[self.cur_source_file] = {}
                self.write(u'{indent}Source path:... '
                           u'{source_path}'.format(**locals()))
                self.last_source_path = source_path
        source_line = source[line_no - 1]
        thread_info = ""
        if self.thread_info:
            if self.normalize:
                raise NotImplementedError("normalize is not supported with "
                                          "thread_info")
            current_thread = threading.current_thread()
            thread_info = "{ident}-{name} ".format(
                ident=current_thread.ident, name=current_thread.name)
        thread_info = self.set_thread_info_padding(thread_info)

        if print_in_this_file:
            old_local_reprs = self.frame_to_local_reprs.get(frame, {})
            self.frame_to_local_reprs[frame] = local_reprs = \
                                           get_local_reprs(frame,
                                                           watch=self.watch, custom_repr=self.custom_repr,
                                                           max_length=self.max_variable_length,
                                                           normalize=self.normalize,
                                                           )

            is_starting_var = event == 'call'
            newish_string = ('Starting var:.. ' if is_starting_var else 'New var:....... ')

            for name, value_repr in local_reprs.items():
                if name not in old_local_reprs:
                    if is_starting_var:
                        self.call_var_list[name] = value_repr
                    self.write('{indent}{newish_string}{name} = {value_repr}'.format(**locals()))
                elif old_local_reprs[name] != value_repr:
                    self.write('{indent}Modified var:.. {name} = {value_repr}'.format(**locals()))

        if event == 'call' and source_line.lstrip().startswith('@'):
            for candidate_line_no in itertools.count(line_no):
                try:
                    candidate_source_line = source[candidate_line_no - 1]
                except IndexError:
                    break

                if candidate_source_line.lstrip().startswith('def'):
                    # Found the def line!
                    line_no = candidate_line_no
                    source_line = candidate_source_line
                    break

        code_byte = frame.f_code.co_code[frame.f_lasti]
        if not isinstance(code_byte, int):
            code_byte = ord(code_byte)
        ended_by_exception = (
                event == 'return'
                and arg is None
                and opcode.opname[code_byte] not in RETURN_OPCODES
        )

        if ended_by_exception:
            self.write('{indent}Call ended by exception'.format(**locals()))
        else:
            if print_in_this_file:
                if event == 'call':
                    # print(source_line)
                    m_func = re.findall(r'\s*def (.*?)\(', source_line)
                    if m_func and len(m_func) > 0:
                        self.cur_func = m_func[0]
                        self.var_logger[self.cur_source_file][self.cur_func] = {'param_vars': self.call_var_list, 'line_no': line_no}
                    self.call_var_list = {}
                # to log
                self.write(u'{indent}{thread_info}{event:9} {line_no:4} {source_line}'.format(**locals()))

        if event == 'return':
            self.frame_to_local_reprs.pop(frame, None)
            thread_global.depth -= 1

            if not ended_by_exception:
                return_value_repr = get_shortish_repr(arg, custom_repr=self.custom_repr,
                                                      max_length=self.max_variable_length,
                                                      normalize=self.normalize,)
                if print_in_this_file:
                    # print(self.var_logger)
                    # print(self.cur_func)
                    self.var_logger[self.cur_source_file][self.cur_func]['return_var'] = return_value_repr
                    self.write('{indent}Return value:.. {return_value_repr}'.format(**locals()))

        if event == 'exception':
            exception = '\n'.join(traceback.format_exception_only(*arg[:2])).strip()
            if self.max_variable_length:
                exception = truncate(exception, self.max_variable_length)
            if print_in_this_file:
                self.write('{indent}Exception:..... {exception}'.format(**locals()))

        return self.trace
