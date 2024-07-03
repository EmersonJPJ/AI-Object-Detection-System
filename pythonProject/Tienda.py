import ComprasIA as shop

def main():
    class_shop = shop.TiendaIA()
    cap = class_shop.init()
    # Stream
    stream = class_shop.tiendaIA(cap)

if __name__ == "__main__":
    main()