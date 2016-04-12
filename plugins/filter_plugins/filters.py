from ansible import errors
from copy import deepcopy
from sets import Set
import json

def dict_merge(a, b):
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def get_ip_from_inv(host_vars, groups, mixin = {}):
    data = {}
    for group in groups:
        if group not in data:
            data[group] = []
            for host in groups[group]:
                data[group].extend(host_vars[host]['ansible_all_ipv4_addresses'])
    data = dict_merge(data, mixin)
    return data

def to_group_vars(host_vars, groups, target = 'all'):
    data = []
    for host in groups[target]:
        data.append(host_vars[host])
    return data

def not_in_list(list, haystack):
    rv = []
    for item in list:
	if item not in haystack:
	    rv.append(item)
    return rv
def add_suf(list, attr):
    rv = []
    for item in list:
        rv.append(item + attr)
    return rv
def _map_on_attr(item, attr, default):
    rv = item
    attr_list = attr.split('.')
    for a in attr_list:
        if rv.has_key(a):
            rv = rv[a]
        else:
            if default:
                return default
            else:
                return False
    return rv
def filter_on_attr(list, attr, invert=False):
    rv = []
    for item in list:
        r = _map_on_attr(item, attr, False);
        if bool(r) ^ invert:
            rv.append(item)
    return rv
def map_on_attr(list, attr, default=False):
    rv = []
    for item in list:
        r = _map_on_attr(item, attr, default);
        if r is not False:
            rv.append(r)
    return rv
def dict_merge(a, b):
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result
def multiple_dict_merge(list_dicts):
    result = {}
    for obj in list_dicts:
        if isinstance(obj, dict) and len(obj):
            result = dict_merge(result, obj)
    return result
def syslog_facility_from_str(list):
    rv = []
    for item in list:
        a = item.split(".");
        rv.append(a[0])
    return rv
def syslog_severity_from_str(list, default=''):
    rv = []
    for item in list:
        a = item.split(".");
        if a[1]:
            rv.append(a[1])
        elif default:
            rv.append(default)
            
    return rv
def syslog_facility_to_prio(string):
    fac_map = dict(
        kern     =  0 ,  
        user     =  1 ,
        mail     =  2 ,
        daemon   =  3 ,
        auth     =  4 ,
        syslog   =  5 ,
        lpr      =  6 ,
        news     =  7 ,
        uucp     =  8 ,
        cron     =  9 ,
        security =  10,
        ftp      =  11,
        ntp      =  12,
        logaudit =  13,
        logalert =  14,
        clock    =  15,
        local0   =  16,
        local1   =  17,
        local2   =  18,
        local3   =  19,
        local4   =  20,
        local5   =  21,
        local6   =  22,
        local7   =  23)
    sev_map = dict(
        emerg   = 0,
        alert   = 1,
        crit    = 2,
        error   = 3,
        warning = 4,
        notice  = 5,
        info    = 6,
        debug   = 7) 
    a = string.split(".");
    if a[0] not in fac_map or a[1] not in sev_map:
        raise errors.AnsibleFilterError('Bad "<facility>.<severity>" pair.')
    return (fac_map[a[0]] * 8) + sev_map[a[1]]

def multiple_dicts(custom_tmpls, counts):
    res = []
    for t in custom_tmpls:
        tmpl = custom_tmpls[t]
        for c in range(counts[t]):
            o = {}
            for p in tmpl:
                o[p] = tmpl[p].replace("%COUNT%", str(c))
            res.append(o)
    return res

def contain_substrs(list, substrs):
    res = []
    for source in list:
        for substr in substrs:
            if substr in source:
                res.append(source)
                break
    return res

def has_attr(list, attr):
    result = []
    attrs_val = attr.split("=")
    attr_val =  None if len(attrs_val) < 2 else attrs_val[1]

    for item in list:
        o = _map_on_attr(item, attrs_val[0], False)
        if o is not False:
            if attr_val == None or attr_val == o:
                result.append(item)
    return result

def is_empty(object):
    return not len(a)

def change_attr(src_dict, path, new_value):
    result = src_dict
    attr_list = path.split('.')
    nesting = 0
    rv = result
    for a in attr_list:
        if isinstance(rv, dict) and rv.has_key(a):
            if nesting == (len(attr_list)-1):
                rv[a] = new_value
            else:
                rv = rv[a]
                nesting += 1
        else:
            return result
    return result


class FilterModule(object):
    def filters(self):
        return {
            'add_suf': add_suf,
            'map_on_attr': map_on_attr,
            'syslog_facility_to_prio': syslog_facility_to_prio,
            'to_group_vars': to_group_vars,
            'dict_merge': dict_merge,
            'not_in_list': not_in_list,
            'multiple_dicts' : multiple_dicts,
            'contain_substrs': contain_substrs,
            'has_attr': has_attr,
            'multiple_dict_merge': multiple_dict_merge,
            'change_attr': change_attr,
            'filter_on_attr': filter_on_attr,
            'get_ip_from_inv': get_ip_from_inv
        }
