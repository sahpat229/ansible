#!/user/bin/python

from ansible.module_utils.basic import *
import requests

def get_lines(file_name):
	is_error = False
	result = []
	has_changed = False
	try:
		with open(file_name, 'r') as file:
			result = list(file)
	except Exception:
		is_error = True
	return (is_error, has_changed, result)


if __name__ = '__main__':
	main()

def main():
	field = {
		"file_name": {"required": True, "type": "str"}
	}

	module = AnsibleModule(argument_spec=field)
	is_error, has_changed, result = get_lines(field["file_name"])
	if not is_error:
		module.exit_json(changed=has_changed, command_list=result)