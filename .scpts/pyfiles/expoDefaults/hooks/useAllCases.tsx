/**
 * handle various cases of strings
 */

const operateOnStr = (str: string, operation: string) => {
	const excempts: string[] = ['is', 'and', 'a']
	const firstChar = str.split(operation).map(word => !excempts.includes(word)?word.charAt(0).toUpperCase():word.charAt(0))
	const otherChars = str.split(operation).map(word => word.slice(1))
	const newStr = firstChar.map((char, index) => char + otherChars[index])
	return newStr.join(operation)
}
// convert string to title case
const toTitleCase = (str: string) => {
	let newStr
	if (str.includes('-')) {
		newStr = operateOnStr(str, '-')
	} else if (str.includes(' ')) {
		newStr = operateOnStr(str, ' ')
	} else {
		newStr = str.charAt(0).toUpperCase() + str.slice(1)
	}
	return newStr
}
export { toTitleCase}