from varasto import Varasto


class VarastoDemo:
    def __init__(self):
        self.mehua = Varasto(100.0)
        self.olutta = Varasto(100.0, 20.2)

    def luonnin_jalkeen(self):
        print("Luonnin jälkeen:")
        print(f"Mehuvarasto: {self.mehua}")
        print(f"Olutvarasto: {self.olutta}")

    def olut_getterit(self):
        print("Olut getterit:")
        print(f"saldo = {self.olutta.saldo}")
        print(f"tilavuus = {self.olutta.tilavuus}")
        print(f"paljonko_mahtuu = {self.olutta.paljonko_mahtuu()}")

    def mehu_setterit(self):
        print("Mehu setterit:")
        print("Lisätään 50.7")
        self.mehua.lisaa_varastoon(50.7)
        print(f"Mehuvarasto: {self.mehua}")
        print("Otetaan 3.14")
        self.mehua.ota_varastosta(3.14)
        print(f"Mehuvarasto: {self.mehua}")

    def virheellinen_tilavuus(self):
        print("Virhetilanteita:")
        print("Varasto(-100.0);")
        huono = Varasto(-100.0)
        print(huono)

    def virheellinen_alkusaldo(self):
        print("Varasto(100.0, -50.7)")
        huono = Varasto(100.0, -50.7)
        print(huono)

    def oluen_ylitaytto(self):
        print(f"Olutvarasto: {self.olutta}")
        print("olutta.lisaa_varastoon(1000.0)")
        self.olutta.lisaa_varastoon(1000.0)
        print(f"Olutvarasto: {self.olutta}")

    def mehun_negatiivinen_lisays(self):
        print(f"Mehuvarasto: {self.mehua}")
        print("mehua.lisaa_varastoon(-666.0)")
        self.mehua.lisaa_varastoon(-666.0)
        print(f"Mehuvarasto: {self.mehua}")

    def oluen_yliotto(self):
        print(f"Olutvarasto: {self.olutta}")
        print("olutta.ota_varastosta(1000.0)")
        saatiin = self.olutta.ota_varastosta(1000.0)
        print(f"saatiin {saatiin}")
        print(f"Olutvarasto: {self.olutta}")

    def mehun_negatiivinen_otto(self):
        print(f"Mehuvarasto: {self.mehua}")
        print("mehua.ota_varastosta(-32.9)")
        saatiin = self.mehua.ota_varastosta(-32.9)
        print(f"saatiin {saatiin}")
        print(f"Mehuvarasto: {self.mehua}")

    def normaalitilanteet(self):
        self.luonnin_jalkeen()
        self.olut_getterit()
        self.mehu_setterit()

    def virhetilanteet(self):
        self.virheellinen_tilavuus()
        self.virheellinen_alkusaldo()
        self.oluen_ylitaytto()
        self.mehun_negatiivinen_lisays()
        self.oluen_yliotto()
        self.mehun_negatiivinen_otto()

    def suorita(self):
        self.normaalitilanteet()
        self.virhetilanteet()


def main():
    demo = VarastoDemo()
    demo.suorita()


if __name__ == "__main__":
    main()
