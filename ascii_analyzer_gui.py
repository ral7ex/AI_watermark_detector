import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class ASCIIAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Character Analyzer")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ASCII Character Analyzer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Options", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # File selection
        ttk.Label(input_frame, text="File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(input_frame, textvariable=self.file_path_var)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)
        ttk.Button(input_frame, text="Analyze File", command=self.analyze_file).grid(row=0, column=3, padx=(5, 0))
        
        # Text input
        ttk.Label(input_frame, text="Or paste text:").grid(row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 5), pady=(10, 0))
        self.text_input = tk.Text(input_frame, height=4, width=50)
        self.text_input.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0), padx=(0, 5))
        ttk.Button(input_frame, text="Analyze Text", command=self.analyze_text).grid(row=1, column=2, sticky=tk.N, pady=(10, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for highlighting
        self.results_text.tag_configure("suspicious", background="yellow", foreground="red")
        self.results_text.tag_configure("header", font=("Consolas", 10, "bold"))
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def analyze_file(self):
        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file first.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found.")
            return
        
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.perform_analysis(text, f"File: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {str(e)}")
    
    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).rstrip('\n')
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            return
        
        self.perform_analysis(text, "Pasted Text")
    
    def perform_analysis(self, text, source):
        self.results_text.delete("1.0", tk.END)
        
        # Analysis header
        header = f"Analysis Results for {source}\n"
        header += f"Text length: {len(text)} characters\n"
        header += "=" * 60 + "\n\n"
        self.results_text.insert(tk.END, header, "header")
        
        # Perform the analysis
        char_frequency = {}
        sus_positions = []
        
        for pos, char in enumerate(text):
            ascii_value = ord(char)
            
            if self.is_sus_ascii(char):
                sus_positions.append((pos, char, ascii_value))
            
            char_info = (char, ascii_value)
            char_frequency[char_info] = char_frequency.get(char_info, 0) + 1
        
        # Display only suspicious characters in frequency table
        sus_chars = [(char, ascii_value, freq) for (char, ascii_value), freq in char_frequency.items() if self.is_sus_ascii(char)]
        
        if sus_chars:
            self.results_text.insert(tk.END, "Suspicious Characters Found:\n", "header")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            self.results_text.insert(tk.END, "Character | ASCII Value | Occurrences\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            
            for char, ascii_value, frequency in sorted(sus_chars, key=lambda x: x[1]):
                display_char = self.get_display_char(char)
                line = f"{display_char:^9} | {ascii_value:^11} | {frequency:^11} (SUS!)\n"
                self.results_text.insert(tk.END, line, "suspicious")
        
        # Display suspicious character analysis
        if sus_positions:
            self.results_text.insert(tk.END, f"\nATTENTION: {len(sus_positions)} suspicious characters found!\n", "suspicious")
            self.results_text.insert(tk.END, "\nFull text with suspicious characters highlighted:\n", "header")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            
            # Display text with highlighting
            current_pos = 0
            for pos, char, _ in sus_positions:
                # Add normal text before suspicious character
                if pos > current_pos:
                    self.results_text.insert(tk.END, text[current_pos:pos])
                
                # Add suspicious character with highlighting
                self.results_text.insert(tk.END, char, "suspicious")
                current_pos = pos + 1
            
            # Add remaining text
            if current_pos < len(text):
                self.results_text.insert(tk.END, text[current_pos:])
            
            self.results_text.insert(tk.END, "\n" + "-" * 50 + "\n")
        else:
            self.results_text.insert(tk.END, "\nNo suspicious characters found.\n")
    
    def is_sus_ascii(self, character):
        ascii_code = ord(character)
        return not (32 <= ascii_code <= 126 or ascii_code == 10)
    
    def get_display_char(self, char):
        if char.isspace():
            if char == ' ':
                return 'SPACE'
            elif char == '\n':
                return '\\n'
            elif char == '\t':
                return '\\t'
        return char

def main():
    root = tk.Tk()
    app = ASCIIAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()