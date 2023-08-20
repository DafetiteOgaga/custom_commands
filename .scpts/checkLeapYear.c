#include <stdio.h>
/* ENTER OTHER HEADER FILES */

/**
 * main - This program checks if the input date is a leap
 * year or not and prints the number of days remaining
 * @parameter1
 * @parameter2
 * ...
 * 
 * Return: 0 for succes
 */

int main(void)
{
	int day, month, year;
	char *leap_year;

	day = 29;
	month = 02;
	year = 2020;

	if (year % 4 == 0)
		if (year % 100 == 0)
			if (year % 400 == 0)
				leap_year = "It is a leap year";
			else
				leap_year = "It is not a leap year";
		else
			leap_year = "It is a leap year";
	else
		leap_year = "It is not a leap year";
	printf("%s\n", leap_year);

	return (0);
}
