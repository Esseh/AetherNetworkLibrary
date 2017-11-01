class resultObject:
	def __init__(self,error,result):
		self.error = error
		self.result = result

# Wraps the exceution of a python function automatically catching the error and passing it up in a C++ readable format.
def executeFunction(function,args):
	global resultMap
	try:
		# If nothing goes wrong then return no error along with the result of the function
		result = resultObject("",function(*args))
		return result
	except Exception as e:
		# Otherwise pass the error up in a format usable by C++.
		errorType = type(e)
		truncatedErrorType = str(errorType)[7:-2]
		result = resultObject(truncatedErrorType, None)
		return result
		
def tostring(a,b):
	return str(a) + str(b)
	
def test(a,b):
	return "hoi"