import string
def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score +=1
    
    levels = {
        1: "Very Weak",
        2: "Weak",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong"
    }

    return levels.get(score, "Extremely Weak")

if __name__=="__main__":
    pwd = input("Enter a password to check: ")
    print(" Strength:", check_password_strength(pwd))