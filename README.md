# TextGeneration
 This is an automatic text generator which uses a simple statistical language model. An approximate algorithm is as follows. At the first stage, the stage of learning, we are on some kind of text array, for example, "Alices Adventures in Wonderland", learn how many times every word w1 occurs after the word w2. At the generation stage, we generate words with the corresponding frequency distribution considering previously generated ones. Likewise, we can generate a words based on the last two words, on the three, and so on.

Following text was used for generating probabilities: [Carroll Lewis - Alices Adventures in Wonderland](https://drive.google.com/file/d/1khBh2dAaTVcYQ2WAESrf6yml0Jx3vub_/view?usp=sharing)

**Description:**
* `probabilities.json` - file with all frequency distribution
* `depth` - the number of considered words which is used to calculate distributions.
* `number_of_tokens` - the number of generated words.
* `uniform_proba` - the probability of generating word considering frequency distribution, 1 - uniform_proba is a probability that next word would be generated considering equiprobable distribution for all possible tokens.
* `mask` - regular expression to define the token. For example “\d+” - only sequences of digits will be tokens.
* `Generate_text` state is interactive. Commands from the console are available. All possible commands are described below.


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
