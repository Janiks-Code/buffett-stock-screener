from buffett_weekly_email import run_buffett_screen, send_email
from strategies.ai_nuclear_growth import run_ai_nuclear_screen

def main():
    buffett_df = run_buffett_screen()
    send_email(buffett_df, "Buffett Value Strategy")

    ai_df = run_ai_nuclear_screen()
    send_email(ai_df, "AI + Nuclear Growth Strategy")

if __name__ == "__main__":
    main()
