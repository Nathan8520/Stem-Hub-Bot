from datetime import datetime
import typing
from discord import Embed, TextChannel
from discord.ext.commands import Bot, Cog, Context, command
import discord.ext.commands as commands
from discord.utils import get
from discord.ext import tasks
import discord

class Dropdown(discord.ui.Select):
    def __init__(self, roles):

        options = []

        for role in roles:
            options.append(discord.SelectOption(label=role [0], value=role [1]))

        super().__init__(
            placeholder="Choose a role to add:",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="reaction-roles-select"
        )

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(int(self.values [0]))

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)

class DropdownView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(roles))

class Reaction(Cog):

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def setupRoles(self, ctx):
        embed = discord.Embed(title="Self roles", description="Use the menus below to give yourself roles.\nJust select the role you want from the options to add it.\nIf you want to remove a role just select it again and it will be removed.")

        await ctx.send(embed=embed)

        view = DropdownView([("helper-algebra", "921739740993171466"),
                             ("helper-geometry", "921739899714035724"),
                             ("helper-statistics", "921761478636359730"),
                             ("helper-calculus", "921761568570617937"),
                             ("helper-uni-maths", "921761630323372052"),
                             ("helper-biology", "921739273827393557"),
                             ("helper-chemistry", "921739350188892220"),
                             ("helper-physics", "921739393247633429"),
                             ("helper-computer science", "921739456506101820"),
                             ("helper-english", "921761704734502992"),
                             ("helper-history", "921761778583605288"),
                             ("helper-geography", "921761857302323280"),
                             ("helper-languages", "921761937707110450")])

        embed= discord.Embed(title="Helper roles", description="Choose which subjects you want to help others in.\nThese roles can be pinged by anyone", color=0x00aaaa)
        await ctx.send(embed=embed, view=view)

    @Cog.listener()
    async def on_ready(self):
        view = discord.ui.View(timeout=None)
        view.add_item(Dropdown([("helper-algebra", "921739740993171466"),
                             ("helper-geometry", "921739899714035724"),
                             ("helper-statistics", "921761478636359730"),
                             ("helper-calculus", "921761568570617937"),
                             ("helper-uni-maths", "921761630323372052"),
                             ("helper-biology", "921739273827393557"),
                             ("helper-chemistry", "921739350188892220"),
                             ("helper-physics", "921739393247633429"),
                             ("helper-computer science", "921739456506101820"),
                             ("helper-english", "921761704734502992"),
                             ("helper-history", "921761778583605288"),
                             ("helper-geography", "921761857302323280"),
                             ("helper-languages", "921761937707110450")]))

        self.bot.add_view(view)




def setup(bot: Bot):
    bot.add_cog(Reaction(bot))