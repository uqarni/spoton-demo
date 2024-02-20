from supabase import create_client, Client
import os

def initialize_prompt_and_text(session_state):
    #connect to supabase database
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)
    data, count = supabase.table("bots_dev").select("*").eq("id", "spencer").execute()
    bot_info = data[1][0]

    system_prompt = bot_info['system_prompt']
    initial_text = bot_info['initial_text']
    to_format = {
        'lead_first_name': session_state.lead_first_name,
        'agent_name': 'Spencer',
        'industry': session_state.industry,
        'company_name': session_state.company_name,
        'booking_link': 'spoton_booking.com'
    }
    initial_text = initial_text.format(**to_format)
    system_prompt = system_prompt.format(**to_format)

    session_state.system_prompt = system_prompt
    session_state.initial_text = initial_text
    session_state.messages.insert(0, {'role': 'assistant', 'content': initial_text})

