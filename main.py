import disnake
from disnake.ext import commands
from disnake import OptionType
from placafipy import PlacaFipy
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter os tokens do arquivo .env
TOKEN = os.getenv('DISCORD_TOKEN')
placafipy_tokens = [
    os.getenv('PLACAFIPY_TOKEN_1'),
    os.getenv('PLACAFIPY_TOKEN_2'),
    os.getenv('PLACAFIPY_TOKEN_3')
]

# Configuração do cliente Discord com Slash Commands
bot = commands.Bot(command_prefix='!', intents=disnake.Intents.default())
placafipy = PlacaFipy(placafipy_tokens)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Comandos Slash
@bot.slash_command(name="estado",
                   description="Obter o estado a partir da sigla",
                   options=[
                       disnake.Option(name="sigla", description="Sigla do estado", type=OptionType.string, required=True)
                   ])
async def estado(ctx, sigla: str):
    await ctx.response.defer()
    estado = placafipy.obter_estado(sigla)
    await ctx.send(f'O estado correspondente à sigla {sigla} é {estado}')

@bot.slash_command(name="mercosul",
                   description="Verificar se uma placa é do modelo Mercosul",
                   options=[
                       disnake.Option(name="placa", description="Placa do veículo", type=OptionType.string, required=True)
                   ])
async def mercosul(ctx, placa: str):
    await ctx.response.defer()
    placa_mercosul = placafipy.verificar_placa_mercosul(placa)
    await ctx.send(f'A placa {placa} é do modelo Mercosul? {placa_mercosul}')

@bot.slash_command(name="converter",
                   description="Conversão de placas",
                   options=[
                       disnake.Option(name="placa", description="Placa a ser convertida", type=OptionType.string, required=True)
                   ])
async def converter(ctx, placa: str):
    await ctx.response.defer()
    placa_convertida = placafipy.converter_placa(placa)
    await ctx.send(f'A placa {placa} foi convertida para {placa_convertida}')

@bot.slash_command(name="Consultar",
                   description="Consultar informações de um veículo pela placa",
                   options=[
                       disnake.Option(name="placa", description="Placa do veículo", type=OptionType.string, required=True)
                   ])
async def info(ctx, placa: str):
    await ctx.response.defer()
    informacoes_veiculo = placafipy.consulta(placa)
    if informacoes_veiculo:
        await ctx.send(f'Informações do veículo com a placa {placa}: {informacoes_veiculo}')
    else:
        await ctx.send('Não foi possível obter informações para a placa especificada.')

# Conectar o bot ao Discord
bot.run(TOKEN)
