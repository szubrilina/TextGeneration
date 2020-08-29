# TextGeneration
 Python HW

**Working version** of code in file: `TextGeneration.py`

Following text was used for generating probabilities: [Carroll Lewis - Alices Adventures in Wonderland](https://drive.google.com/file/d/1khBh2dAaTVcYQ2WAESrf6yml0Jx3vub_/view?usp=sharing)

**Examples of running programm:**
* text generation:  
    `generate_text --probabilities_file <filename.json> --depth <int> --output_file <filename.txt> --number_of_tokens <int> --uniform_proba <float>`

  if *output_file* is not state, then it prints result in console  

  if *uniform_proba* is not state, default value is 0  


* counting probabilities:  
    `calculate_probabilities --mask \d+ --input_file <filename1.txt> --probabilities_file <filename2.json> --depth <int>`
    
* availadle commands:


   `--help`
   
   `generate number<int>`
       generate text with number tokens

   `clear`
       clear current history

   `set_history new_history<string>`
       current history is set equal to new_history

   `observe_history`
       print current history

   `change_depth number<int>`
       current depth is made to be equal number

   `probabilities`
       print probabilities for the next token

   `finish`
       exite programm

---

**Examples of result:**  

Rabbit moment. "I never was so her how she would feel very queer to me! 
There was a queer-shaped little creature, but said nothing the proper and
the others all joined in chorus"!  


All spoke at once the thimble, saying to herself "It’s all his fancy sneezes; 
was to eat the comfits: this fireplace nearer to of history, you know—" 
She boxed the Queen's voice in the schoolroom, and she went back for a dunce all 
directions the Gryphon, and giving and waited to to be in. The Rabbit sends in a moment.
