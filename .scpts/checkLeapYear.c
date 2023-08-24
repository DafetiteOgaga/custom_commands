#include <stdio.h>
#define LENGTH(arr) (sizeof(arr)/sizeof(arr[0]))
/* ENTER OTHER HEADER FILES */

/**
 * main - This program checks if the input date is a leap
 * year or not and prints the number of days remaining
 * t - target
 * @parameter1
 * @parameter2
 * ...
 * 
 * Return: 0 for succes
 */
int leapYearFunc(int, int, int);
int main(void)
{
	int user_inp_day, user_inp_month, user_inp_year;
	int i, j, leapY, max_days, rem_days, len;
	int daysMonth[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	int t_day, t_month, t_year;
	char *leap_year;
	

	user_inp_day = 22;
	user_inp_month = 8;
	user_inp_year = 2023;

	t_day = 5;
	t_month = 12;
	t_year = 2023;

	len = LENGTH(daysMonth);

	/* leap year */
	leapY = leapYearFunc(user_inp_day, user_inp_month, user_inp_year);
	printf("%02d-%02d-%02d\n", user_inp_day, user_inp_month, user_inp_year);

	/* second month */
	if (user_inp_month == 2 && leapY)
		max_days = 29;
	else
		max_days = daysMonth[user_inp_month - 1];
	
	/* remove */
	int l = 0;
	for (int k = 0 ; k < len ; k++)
		l += daysMonth[k];
	if (leapY)
			l += 1;
	/* remove */

	/* remaining days */
	if (user_inp_day <= max_days)
	{
		/* days/months elapsed */
		int daysLapsed = user_inp_day;
		for (int month = 1 ; month < user_inp_month ; month++)
			daysLapsed += daysMonth[month - 1];

		printf("............................\n");
		int t_leapY = leapYearFunc(t_day, t_month, t_year);
		printf("%02d-%02d-%02d\n", t_day, t_month, t_year);

		/* remove */
		printf("daysLapsed = %d\n", daysLapsed);
		/* remove */

		/* t_max days in month */
		int t_maxDays;
		if (t_month == 2 && t_leapY)
			t_maxDays = 29;
		else
			t_maxDays = daysMonth[t_month - 1];

		if (t_day <= t_maxDays)
		{
			//......................................
			printf("............................\n");
			/* remaining days */
			int t_rem_days = t_day;
			for (int monthC = t_month - 1 ; monthC >= 1 ; monthC--)
				t_rem_days += daysMonth[monthC - 1];

			printf("t_rem_days = %d\n", t_rem_days);

			int total_days_btw = 0;
			for (int year = user_inp_year ; year < t_year ; year++)
			// for (int year = user_inp_year + 1 ; year < t_year ; year++)
			{
				if (user_inp_year % 4 == 0 && (user_inp_year % 100 != 0 || user_inp_year % 400 == 0))
					total_days_btw += 366;
				else
					total_days_btw += 365;
			}

			printf("total_days_btw = %d\n", total_days_btw);


			if (t_month > user_inp_month || (t_month == user_inp_month && t_day >= user_inp_day))
				total_days_btw += t_rem_days - daysLapsed;
			else
				total_days_btw -= daysLapsed;

			printf("Total days betwen the days = %d\n", total_days_btw);




			// rem_days += max_days - user_inp_day;
			// printf("Remaining days is %d\n", rem_days);

			// printf("Days spent %d - %d = %d\n", l, rem_days, l - rem_days);
		}
		else
			printf("Invalid date\n");
	}
	else
		printf("Invalid date\n");


	return (0);
}

/**
 * main - This program checks if the input date is a leap
 * year or not and prints the number of days remaining
 * @parameter1
 * @parameter2
 * ...
 * 
 * Return: 0 for succes
 */
int leapYearFunc(int uday, int umonth, int uyear)
{
	char *leap_year;
	int leapY;

	if (uyear % 4 == 0 && (uyear % 100 != 0 || uyear % 400 == 0))
	{
		leapY = 1;
		leap_year = "is a leap year";
	}
	else
	{
		leapY = 0;
		leap_year = "is not a leap year";
	}
	printf("from function: %02d-%02d-%02d %s\n", uday, umonth, uyear, leap_year);

	return (leapY);
}