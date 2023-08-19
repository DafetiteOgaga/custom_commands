#include <stdio.h>
#define NEWLINE 4

/**
 * main - This program prints the decimal
 * to character of the ascii table
 * Return: 0 for success
 */

int printer(int num);
int main (void)
{
	int digits = 32, res;

	putchar('\n');
	putchar('\t');
	printf("ASCII-TABLE(DECIMAL TO CHARACTERS)");
	putchar('\n');
	putchar('\n');

	printf("...............................................\n");
	for (; digits <= 127; digits++)
	{
		if (digits >= 32 && digits <= 99)
			res = printer(digits);

		else
			res = printer(digits);

		if (res)
			printf("...................................................\n");
	}
	printf("\nD\n");
	return (0);
}

int printer (int num)
{
	int newline;

	printf("%d == '%c' | ", num, num);
	if ((num + 1) % NEWLINE == 0)
		printf("\n");

	newline = (num == 99 || num == 127) ? 6 : 0;

	return (newline);
}
