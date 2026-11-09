import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import pytest


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

# Va todo lo de la pagina, localizadores, metodos (acciones)
class UrbanRoutesPage:
    #--- Campos de dirección-------
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    #---------- Pedir taxi y tarifa---------------------
    order_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_button = (By.XPATH, "//div[text()='Comfort']")

    #---------- Teléfono -------------------------------
    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    phone_input = (By.ID, "phone")
    next_button = (By.XPATH, "//button[text()='Siguiente']")
    code_input = (By.ID, "code")
    confirm_button = (By.XPATH, "//button[text()='Confirmar']")

    #---------- Tarjeta de credito -----------------------
    payment_method_button = (By.XPATH, "//div[contains(@class,'pp-button') and .//div[text()='Método de pago']]")
    add_card_button = (By.XPATH, "//div[contains(text(),'Agregar tarjeta')]")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//input[@id='code' and contains(@class,'card-input')]")
    confirm_add_card_button = (By.XPATH, "//button[text()='Agregar']")
    close_card = (By.XPATH, "//button[contains(@class,'close-button')]")

    #-------- Mensaje conductor --------------------------
    message_input = (By.ID, "comment")

    #-------- Manta y pañuelos ---------------------------
    blanket_switch = (By.XPATH, "//div[@class='switch']/input[@class='switch-input']")

    # ── Helados ─────────────────────────────────────────────────────
    ice_cream_plus = (By.XPATH, "//div[@class='counter-plus']")
    ice_cream_count = (By.XPATH, "//div[@class='counter-value']")

    # ── Botón final pedir taxi ───────────────────────────────────────
    order_taxi_button_final = (By.XPATH, "//button[@class='smart-button']")
    search_modal = (By.XPATH, "//div[contains(@class,'order-header-title')]")

    # --- información del conductor ---------------------------
    driver_info = (By.XPATH, "//div[contains(@class,'order-btn-rating')]")

    def __init__(self, driver):
        self.driver = driver

    #--------- Dirección --------------------------
    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_adress, to_adress):
        self.set_from(from_adress) #metodo para escribir dirección, hace click en algo y luego selecciona algo
        self.set_to(to_adress)

    #--- Taxi y tarifa ---------------------------------------
    def click_order_taxi(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_button))
        element.click()

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_button)).click()

    def is_comfort_selected(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.comfort_button)
        )
        parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class,'tcard')]")
        return "active" in parent.get_attribute("class")

    #--- Teléfono --------------------------------------------
    def click_phone_button(self):
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(self.phone_button)
        ).click()

    def set_phone(self, phone_number):
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(self.phone_input)
        ).send_keys(phone_number)

    def click_next_phone(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.next_button)
        ).click()

    def set_phone_code(self):
        code = retrieve_phone_code(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.code_input)
        ).send_keys(code)

    def confirm_phone_code(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.confirm_button)
        ).click()

    # ------ Tarjeta de credito -------------
    def click_payment_method(self):
        element = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)

    def add_card(self, card_number, card_code):
        self.click_payment_method()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_number_input)
        ).send_keys(card_number)

        cvv = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        )
        cvv.send_keys(card_code)
        cvv.send_keys(Keys.TAB)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.confirm_add_card_button)
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(self.card_number_input)
        )

        close_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.close_card)
        )
        self.driver.execute_script("arguments[0].click();", close_btn)

        # ← ESTO ES LO NUEVO: esperar que el overlay desaparezca
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "overlay"))
        )

    def is_card_added(self):
        """Verifica que aparezca 'Tarjeta' como método de pago activo."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'pp-button')]//div[contains(text(),'Tarjeta')]")
                )
            )
            return element is not None
        except Exception:
            return False

    # --- Mensaje conductor ---------------------------
    def set_message(self, message):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.message_input)
        )
        element.clear()
        element.send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.message_input).get_property('value')

    # ---- Manta y pañuelos ----------------------------
    def click_blanket_switch(self):
        """Activa el toggle de Manta y pañuelos."""
        switch = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.blanket_switch)
        )
        self.driver.execute_script("arguments[0].click();", switch)

    def is_blanket_active(self):
        switch = self.driver.find_element(*self.blanket_switch)
        return switch.is_selected()

    #---- Pedir helados --------------------------------

    def add_ice_cream(self, quantity=2):
        for _ in range(quantity):
            btn = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located(self.ice_cream_plus)
            )
            self.driver.execute_script("arguments[0].click();", btn)

    def get_ice_cream_count(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.ice_cream_count)
        )
        return int(element.text)

    #------- reserva de taxi ----------------------
    def click_order_final(self):
        btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.order_taxi_button_final)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def is_search_modal_shown(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                expected_conditions.visibility_of_element_located(self.search_modal)
            )
            return element is not None
        except Exception:
            return False

    def wait_for_driver_info(self, timeout=60):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                expected_conditions.visibility_of_element_located(self.driver_info)
            )
            return element is not None
        except Exception:
            return False

# van los test, pasos del usuario, asserts
class TestUrbanRoutes:
    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        # se debio modificar ya que selenium 4 ya no usa la anterior forma y es necesario usar la correspondiente a nuevas versiones
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options) #inicialización de selenium , abre chrome , configura logs
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)


    #--- Test 1 Configurar dirección ----------------------
    def test_set_route(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    #--- Test 2 Seleccionar tarifa comfort ---------------
    def test_select_comfort(self):
        self.routes_page.click_order_taxi()
        self.routes_page.select_comfort()
        assert self.routes_page.is_comfort_selected(), "La tarifa Comfort no fue seleccionada"

    #--- Test 3 Rellenar número de telefono --------------
    def test_fill_phone_number(self):
        self.routes_page.click_phone_button()
        self.routes_page.set_phone(data.phone_number)
        self.routes_page.click_next_phone()
        self.routes_page.set_phone_code()
        self.routes_page.confirm_phone_code()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.ID, "code"))
        )
        # Si llega aquí sin excepción, el teléfono fue confirmado correctamente
        assert True

    #--- Test 4 agregar tarjeta de credito ------------
    def test_add_card(self):
        self.routes_page.add_card(data.card_number, data.card_code)

        # Esperar explícitamente que la UI esté estable antes de continuar
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'pp-button')]//div[contains(text(),'Tarjeta')]")
            )
        )

        assert self.routes_page.is_card_added(), "La tarjeta no aparece como método de pago"

    #--- Test 5 Escribir mensaje al conductor ----------
    def test_set_message_for_driver(self):
        self.routes_page.set_message(data.message_for_driver)
        assert self.routes_page.get_message() == data.message_for_driver

    # --- Test 6 Pedir manta y pañuelos
    def test_request_blanket_and_tissues(self):
        self.routes_page.click_blanket_switch()
        assert self.routes_page.is_blanket_active(), "Manta y pañuelos no fue activado"

    # ── Test 7: Pedir 2 helados ──────────────────────────────────────

    def test_request_ice_cream(self):
        self.routes_page.add_ice_cream(2)
        assert self.routes_page.get_ice_cream_count() == 2, "No se agregaron 2 helados"

    # ── Test 8: Aparece modal de búsqueda ────────────────────────────

    def test_order_modal_appears(self):
        self.routes_page.click_order_final()
        assert self.routes_page.is_search_modal_shown(), "El modal de búsqueda no apareció"

    # --- Que aparezca la información del conductor -----------------
    # Test
    def test_driver_info_appears(self):
        assert self.routes_page.wait_for_driver_info(60), "La información del conductor no apareció"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
