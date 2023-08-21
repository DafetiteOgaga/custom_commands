#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/**
 * main - this program guides the user
 * towards guessing the correct answer
 * in 3 guesses.
 * Return: 0 for success
 */
void guessGame (void);
int main (void)
{
	int start;
	char resp;

	start = 0;

	printf("Guess the Lucky number(0-9): \n");
	printf("You have 3 tries:\n\n");

	do
	{
		guessGame ();

		printf("Play again? [n]-quit or [anything]-continue: ");
		scanf(" %c", &resp);

		start = (resp == 'N' || resp == 'n') ? 0 : 1;

		putchar('\n');
	}
	while (start != 0);

	printf("Hope you enjoyed the game.\nCheers\n\n");

	return (0);
}


/**
 * guessGame - This function asks a user
 * to guess the random number in 3 tries
 */
void guessGame (void)
{
	int guess, loopcnt, base, n, luckyNum, len, clr;
	char input[10], *sing = "try", *plur = "tries", *fom;

	srand(time(0));
	n = rand() - RAND_MAX / 2;
	
	if (n < 0)
		luckyNum = (n % 10) * -1;
	else
		luckyNum = (n % 10);

	base = 1;
	loopcnt = 0;

	while (base && loopcnt < 3)
	{
		printf("Guess: ");

		if (scanf("%d", &guess) != 1)
		{
			while ((clr = getchar()) != '\n' && clr != EOF);
			base = 2;
			break;
		}

		if (guess >= 0 && guess <= 9)
		{
			if (guess == luckyNum)
				base = 0;
			else if (guess > luckyNum)
				printf("The number is less than that\n");
			else
				printf("The number is greater than that\n");
		}
		else
			printf("Invalid entry. Only 0-9, pls.\n");

		loopcnt++;
	}
	putchar('\n');

	if (base == 2 || !(guess >= 0 && guess <= 9))
	{
		if (base == 2)
			printf("Invalid input. Please enter a number.\n");
		else
			printf("Invalid input(Only 0-9)\n");
	}

	else if (base == 0 && guess == luckyNum)
	{
		fom = (loopcnt > 1) ? plur : sing;
		printf("Bravo! You won in %d %s\n", loopcnt, fom);
	}

	else
	{
		printf("Oops! You've exhausted %d tries\n", loopcnt);
		printf("The Lucky number is %d\n", luckyNum);
	}
	putchar('\n');
}
