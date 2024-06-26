import json
from hnt_sap_gui import SapGui
from hnt_sap_gui.nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction

def test_create():
    with open("./devdata/json/nota_pedido_GHN-728.json", "r", encoding="utf-8") as nota_pedido_arquivo_json: nota_pedido = json.load(nota_pedido_arquivo_json)
    with open("./devdata/json/miro_GHN-728.json", "r", encoding="utf-8") as miro_arquivo_json: miro = json.load(miro_arquivo_json)

    data = {
        "nota_pedido": nota_pedido,
        "miro": miro,
    }

    issue_key = 'GHN-728'

    result = SapGui(screenshots_on_error=True, screenshot_directory=f'./output/print/{issue_key}').hnt_run_transaction(data)
    assert result is not None
