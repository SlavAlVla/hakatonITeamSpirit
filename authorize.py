import vk_api
from vk_api.longpoll import VkLongPoll
from data_base import get_registration_date, new_user, is_user_already_registered
from datetime import datetime

# Создание главного класса авторизации
# vk1.a.BUhZYAUErvxdTBcOJm8Icwq06hUyLzuz1lh8r4Mi3xrhfxc2tsSPMET_pMM_zQSO7bPrtjqS6VwO4YQ0iPnhAgwz1XWXRtM7-BkC99qz-UHHhvqxorhRabaJESPV98MyXhq9sjydFA8sd5e9oJm2DwbCrSFTFWw_MUMgaxNFw6Uv8zkXeCJ7dcJpb1Limkk52iGVjjhpZLKOym_QTx80sA
token = "vk1.a.fMF3prdIgJWhfaBwIy4Y9Syar_oOPqk8K1bK3CnGsqSiArq7CTg3YkBxVf9KPh8GSY8oPauuIgGS7DSnKV5gOwuhrPqAbEPVxeRKKzmPD3jqVsPvN8UuigrGzR3-yYZBfYHJmqCzvFJTxunJsLSQswwKmw9Hi8dqbMOCXsKjfb1MEjVPJNw6ffIGVe0nCMbeYdEk2yc4QNRz9qYfSvPtlA"
authorize = vk_api.VkApi(token = token)

# Создание лонгполла (API)
longpoll = VkLongPoll(authorize)

# Получить id вопроса
async def get_task_id(sender):
    if (not await is_user_already_registered(sender)):
        await new_user(sender)
    reg_date_str = await get_registration_date(sender)
    reg_date = datetime.strptime(str(reg_date_str[0][0]), '%Y-%m-%d')
    return 29# ((datetime.today() - reg_date).days)%30