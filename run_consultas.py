# run_consultas.py

from app import create_app
from app.models.usuario import Usuario

def main():
    app = create_app()

    with app.app_context():
        # 1) Obtener e imprimir todos los usuarios
        usuarios = Usuario.query.all()
        if usuarios:
            print("=== Todos los Usuarios ===")
            for u in usuarios:
                print(f"ID: {u.usuario_id}")
                print(f"  Nombre completo: {u.primer_nombre} {u.segundo_nombre or ''} {u.primer_apellido} {u.segundo_apellido or ''}")
                print(f"  Fecha Nac.:       {u.fecha_nacimiento}")
                print(f"  Correo:           {u.correo}")
                print(f"  Contraseña:       {u.contraseña}")
                print(f"  Teléfono:         {u.telefono}")
                print(f"  Dirección:        {u.direccion}")
                print(f"  Especialidad:     {u.especialidad}")
                print(f"  Fecha Registro:   {u.fecha_registro}")
                print("-" * 30)
        else:
            print("No se encontraron usuarios.")

        # 2) Pedir al usuario por consola un ID para buscar
        try:
            entrada = input("Ingrese el ID de usuario a buscar (o deje vacío para salir): ").strip()
            if entrada:
                usuario_id = int(entrada)
                usuario = Usuario.query.get(usuario_id)
                if usuario:
                    print("\n=== Usuario Encontrado ===")
                    print(f"ID: {usuario.usuario_id}")
                    print(f"Nombre completo: {usuario.primer_nombre} {usuario.segundo_nombre or ''} {usuario.primer_apellido} {usuario.segundo_apellido or ''}")
                    print(f"Fecha Nac.:       {usuario.fecha_nacimiento}")
                    print(f"Correo:           {usuario.correo}")
                    print(f"Contraseña:       {usuario.contraseña}")
                    print(f"Teléfono:         {usuario.telefono}")
                    print(f"Dirección:        {usuario.direccion}")
                    print(f"Especialidad:     {usuario.especialidad}")
                    print(f"Fecha Registro:   {usuario.fecha_registro}")
                else:
                    print(f"No se encontró usuario con ID {usuario_id}.")
        except ValueError:
            print("El ID ingresado no es un número válido. Saliendo.")

if __name__ == "__main__":
    main()
