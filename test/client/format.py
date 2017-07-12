def input_format(argv_list):
	ret = ''
	for item in argv_list:
		ret = ret + item + '$'
	return ret[:len(ret)-1]
### End of function