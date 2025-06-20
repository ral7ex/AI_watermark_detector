def is_sus_ascii(character) -> bool:
    # Check if the character is a printable ASCII character
    # source for what are normal characters: https://www.ascii-code.com/'
    ascii_code = ord(character)
    if 32 <= ascii_code <= 126 or ascii_code==10:
        return False
    else:
        return True

# ANSI escape codes for colors
RED = '\033[91m'
YELLOW_BG = '\033[103m'
BLACK = '\033[30m'
RESET = '\033[0m'

def analyze_ascii_frequency(text):
    # Initialize a dictionary to store character frequencies
    char_frequency = {}
    sus_positions = []
    
    # Iterate through each character in the text
    for pos, char in enumerate(text):
        # Get ASCII value of the character
        ascii_value = ord(char)
        
        # Check if character is suspicious
        if is_sus_ascii(char):
            sus_positions.append((pos, char, ascii_value))
        
        # Create a tuple of (character, ascii_value) as the dictionary key
        char_info = (char, ascii_value)
        
        # Increment the frequency count
        char_frequency[char_info] = char_frequency.get(char_info, 0) + 1

    # Print the frequency table
    print("\nASCII Character Frequency Table:")
    print("-" * 50)
    print("Character | ASCII Value | Occurences")
    print("-" * 50)
    
    # Sort by ASCII value for consistent output
    for (char, ascii_value), frequency in sorted(char_frequency.items(), key=lambda x: x[0][1]):
        # Handle special characters for display
        display_char = char
        if char.isspace():
            if char == ' ':
                display_char = 'SPACE'
            elif char == '\n':
                display_char = '\\n'
            elif char == '\t':
                display_char = '\\t'
        
        # Add color highlighting for suspicious characters
        if is_sus_ascii(char):
            display_char = f"{YELLOW_BG}{BLACK}{display_char}{RESET}"
            sus_indicator = f" {RED}(SUS!){RESET}"
        else:
            sus_indicator = ""
            
        print(f"{display_char:^9} | {ascii_value:^11} | {frequency:^9}{sus_indicator}")

    if sus_positions: # if we found sus stuff
        print("\nATTENTION: Suspicious characters found!")
        # Print the full text with highlighted suspicious characters
        print("\nFull text, with suspicious characters:")
        print("-" * 50)
        
        # Create a highlighted version of the text
        highlighted_text = text
        for pos, char, _ in reversed(sus_positions):  # Process in reverse to avoid position shifts
            # Insert highlighting around suspicious characters
            highlighted_text = (
                highlighted_text[:pos] + 
                f"{YELLOW_BG}{BLACK}{char}{RESET}" + 
                highlighted_text[pos + 1:]
            )
        
        print(highlighted_text)
        print("-" * 50)

    else: # nothing was found, text is free of sus stuff
        print("\nNo suspicious characters found.")

def process_file(file_path):
    """
    Wrapper function to process a text file and analyze its contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            print(f"\nProcessing file: {file_path}")
            print(f"File size: {len(text)} characters")
            analyze_ascii_frequency(text)
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")

def main():
    '''
    Change the file path as needed. Or, create an ai_testing.txt file right next to this file
    '''
    file_path = "Documents/Code/Fun_Box/AI_Watermarking_Project/ai_testing.txt"
    process_file(file_path) 

if __name__ == "__main__":
    main()
