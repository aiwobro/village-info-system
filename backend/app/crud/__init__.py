from app.crud.admin_village import get_all, get_by_id, create, update, delete
from app.crud.natural_village import get_all as get_all_nv, get_by_id as get_by_id_nv, create as create_nv, update as update_nv, delete as delete_nv
from app.crud.household import get_all as get_all_hh, get_by_id as get_by_id_hh, create as create_hh, update as update_hh, delete as delete_hh
from app.crud.villager import get_all as get_all_v, get_by_id as get_by_id_v, create as create_v, update as update_v, delete as delete_v
from app.crud.contact import get_all as get_all_c, get_by_id as get_by_id_c, create as create_c, update as update_c, delete as delete_c
from app.crud.bank_account import get_all as get_all_b, get_by_id as get_by_id_b, create as create_b, update as update_b, delete as delete_b

__all__ = [
    "get_all", "get_by_id", "create", "update", "delete",
]
