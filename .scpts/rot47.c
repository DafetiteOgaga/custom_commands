#include <stdio.h> 
#include <string.h>

/**
 * main - This program encode, decode, count input
 * characters and tells the number of operation per
 * execution.
 * The cipher works with alphabets and symbols
 * follows the rot47 standard format.
 */

char *cipher (char *par);
int loopFunc (void);
int charCounter (char *cou);
int main() 
{
	int numLoop;

	printf("Enter your text\nIN>>>  ");
	numLoop = loopFunc ();
	printf("\nYou performed %d cipher operation(s)\n", numLoop);
	printf("Cheers\n");

	return 0; 
}


char *cipher (char *par)
{
	int i=0;

	while (par[i] != '\0')
	{
		for (char n='!'; n<='~'; n++)
		{
			if (par[i] == n)
			{
				if (n>=' ' && n<='O')
				{
					par[i] += 47;
					break;
				}

				else if (n>='P' && n<='~')
				{
					par[i] -= 47;
					break;
				}
			}
		}
        i++;
	}
	return par;
}


int loopFunc (void)
{
	char *crypt, user[2001];
	int counter, i=0;

	while (1)
	{
		if (i != 0)
			printf("Go again. Use \"q\" to quit\nIN>>>  ");

		fgets(user, sizeof(user), stdin);

		if ((strlen(user)-1)==1 && *user=='q')
			break;
		
		crypt = cipher (user);
		counter = charCounter (user);

		printf("OUT>>  %s", crypt);
		printf("You entered %d characters.\n\n", counter);
		i++;
	}
	return i;
}


int charCounter (char *cou)
{
	int numChars = (strlen (cou) - 1);
	return numChars;
}
