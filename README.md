# PyWordle
Playing around with wordle mostly inspred by an implementation from [Cameron Riddlle](https://twitter.com/RiddleMeCam) (thanks). This was mostly used to stress-test my neovim config ;). 

On the way I had a stupid bug with mutable state, so I moved some of the old code to the `oop_archive` subfolder and refactored the
state handling a bit restricting mutation to a dedicated `update_state()` function. 


