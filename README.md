# PyBot 
This is an interactive Discord bot written in python. 

#### Functions :
1. Play songs
2. Current Weather
3. Weather Forecast upto 16 days
4. Currency Exchange

# Configuration

__Open the mainboy.py with any editor of your choice__ 

#### Token
_TOKEN_ is your bot token which you'll get after creating your bot. 
To create your own bot/application 
[Discord Developer Portal](https://discordapp.com/developers/applications/)


#### OpenWeatherMap API
__openweatherkey__ refers to your openweathermap API key
you can register an account and get your key [here](https://home.openweathermap.org/users/sign_up)


#### Bot Commnad Prefix 
__PREFIX__ is a tuple, which contains characters by which the bot can be summoned. These characters are to be used before a given commnad _syntax_ : _<prefix><command>_

The default prefixes are : _!,?,|_

### Commands and Syntaxes 
__Note : The following commands use ! as prefix__
  #### Play a youtube song or search for one
     Play a song : !play <song-link> or !play <name-of-the-song>
     example : !play Post Malone Better Now
     
  #### Get the Current Weather in a particular place
     Currenet Weather: !weather <name-of-city>
     example : !weather Mumbai
     
  #### Get the Forecast for upto 16 days for a place
     Forecast Weather: !forecast <name-of-city> <no-of-days>
     example : !forecast Mumbai 7
     
  #### Convert Currency
      Currency Exchange : !exch <from-currency> <to-currency> <amount>
      example !exch USD INR 10

_For help, type **!help** and a list of commands and syntaxes will be given_␏
