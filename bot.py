import discord
from discord.ext import commands
from discord.ui import Select, View
from API_requests import fetch_data, fetch_stream_link_movie
import os
from dotenv import load_dotenv



intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='/', intents=intents)


load_dotenv()
token = os.getenv('Discord_bot_Token')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')


#first solution is to make a list of embed messages 
#which will be populated using a loop and the methods from the API_requests.py 
#that will be sent to the client using another loop and using the  
#{{{await interaction.response.send_message(embed=embed_movie_count)}}} function


@bot.tree.command(name="subtitle",description="Search for a subtitle for a movie using the IMDB code.")
async def slash_command(interaction:discord.Interaction, movie_code:str, language:str):
    await interaction.response.send_message(f"This command is comming soon", ephemeral = True)


@bot.tree.command(name="whatsnew",description="info about the latest update for movix")
async def slash_command(interaction:discord.Interaction):
    help_embed = discord.Embed(title="Movix Version History", description="A list of versions for the Movix bot | (Current) Version 1.2", color=0xffffff)
    help_embed.set_author(name="Movix", icon_url=None)
    help_embed.add_field(name="v1.2 - Get movie stream link", value="Get a stream link for a movie using the movie code use /search to get the movie code.", inline=False)
    
    help_embed.set_footer(text=f"Request made by @{interaction.user.name}", icon_url=f"{interaction.user.avatar.url}")
    await interaction.response.send_message(embed=help_embed)

@bot.tree.command(name="help",description="Help me")
async def slash_command(interaction:discord.Interaction):
    help_embed = discord.Embed(title="Movix help desk.", description="A list of commands for the Movix bot | Version 1.2", color=0xffffff)
    help_embed.set_author(name="Movix", icon_url=None)
    help_embed.add_field(name="/movies - Get all movies", value="Get information about movies.", inline=False)
    help_embed.add_field(name="/stream - Get a stream link to watch", value="Get a stream link for a movie using the movie code use /search to get the movie code", inline=False)
    help_embed.add_field(name="/subtitles - Get a subtitle for a movie", value="Comming soon", inline=False)
    help_embed.set_footer(text=f"Request made by @{interaction.user.name}", icon_url=f"{interaction.user.avatar.url}")
    await interaction.response.send_message(embed=help_embed)
    

@bot.tree.command(name="movie",description="Search for a movie")
async def slash_command(interaction:discord.Interaction, movie_name:str):

    #get data from api
    movies_status = fetch_data(movie_name)
    #handle the error that no movies have been found
    if (movies_status==-1):
        embed_movie_error = discord.Embed( description=f"No movies have been found for {movie_name} :(" ,color=0xFF0000)
        await interaction.response.send_message(embed=embed_movie_error)
        return
    else:
        movie_count = fetch_data(movie_name)['data']['movie_count']
        movies = fetch_data(movie_name)['data']['movies']
        embed_movie_success_movie_count = discord.Embed( description="I have found : "+str(movie_count) +" movie(s)" ,color=0x00FF00)
        
        await interaction.response.defer()
        await interaction.followup.send(embed=embed_movie_success_movie_count)
        
        embed_movie_success = discord.Embed(description=f"Search result for {movie_name}" ,color=0x00FF00)
        for movie in movies:
            #get the torrents infos and populate the select var
            torrents = movie['torrents']
            qualities =[]
            i = 0
            for torrent in torrents:
                #a simple counter to avoid label duplication issue, since it needs to be unique.
                i+=1
                qualities.append(discord.SelectOption(label=f"{i} • {str(torrent['type']).capitalize()} {torrent['quality']} {torrent['video_codec']}",
                                                      description=f"{torrent['size']} | {torrent['peers']} peers | {torrent['seeds']} seeds",
                                                      value=torrent['url']
                                                      ))
                
            
            select = Select(options = qualities, placeholder="Choose a quality for the torrent")
            menu_view = View()
            menu_view.add_item(select)
            #generate the hyperlink for the read more link
            read_more = 'Read more'
            imdb_url = f"https://www.imdb.com/title/{movie['imdb_code']}"
            read_more_hyper_link =  f'[{read_more}]({imdb_url})'
            embed_movie_success.set_thumbnail(url=movie['large_cover_image'])
            embed_movie_success.add_field(name = f"{movie['title_long']}",
                                          value =f"{movie['summary']}"[0:400]+"..."+f"{read_more_hyper_link}",
                                          inline=False)
            
            embed_movie_success.add_field(name = f"Rating",
                                          value =f"{movie['rating']}/10",
                                          inline=True)
            
            embed_movie_success.add_field(name = f"Genres",
                                          value =f"{movie['genres'][0]}",
                                          inline=True)
             
            embed_movie_success.add_field(name = f"Trailer",
                                          value =f"https://www.youtube.com/watch?v={movie['yt_trailer_code']}",
                                          inline=True)
            
            embed_movie_success.add_field(name = f"IMDB code",
                                          value =f"{movie['imdb_code']}",
                                          inline=True)
            
            embed_movie_success.set_footer(text=f"Request made by @{interaction.user.name}", icon_url=f"{interaction.user.avatar.url}")
            await interaction.followup.send(embed=embed_movie_success, view=menu_view)

            async def select_callback(interaction):
                selected_option = interaction.data['values'][0]
                await interaction.response.send_message(f"Downloading torrent from {selected_option}", ephemeral = True)
            
            select.callback = select_callback

            embed_movie_success.clear_fields()
            qualities.clear()
            torrents.clear()
            menu_view.clear_items()


@bot.tree.command(name="steam",description="Stream a movie using the movie imdb or tmdb movie code e.g, tt0075314 | search for the movie using /search <Movie name>.")
async def slash_command(interaction:discord.Interaction, movie_code:str):
    movie_link = fetch_stream_link_movie(movie_code)
    if movie_link != 404:
        embed_movie_success = discord.Embed(description=f"Here is your Steam link for {movie_code}" ,color=0x00FF00)
        embed_movie_success.add_field(name="Link",
                                      value=f"{movie_link}")
        await interaction.response.send_message(embed=embed_movie_success)
    if movie_link == 404:
        embed_movie_error = discord.Embed(description=f"No result for {movie_code}" ,color=0xFF0000)
        await interaction.response.send_message(embed=embed_movie_error)
        
bot.run(token)
