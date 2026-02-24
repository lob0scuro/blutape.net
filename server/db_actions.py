from app.models import Machine, MachineNote, User, WorkOrder, WorkOrderEvent, Base, RoleEnum
from app.extensions import db, bcrypt
from app import create_app

def scorched_earth():
    app = create_app()
    with app.app_context():
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)
        print("DB Has been reset...")
        

def load_me():
    me = User(
        first_name="Cameron",
        last_name="Lopez",
        email="cameron@mattsappliancesla.net",
        role=RoleEnum.ADMIN,
        password_hash=bcrypt.generate_password_hash("Claire18!").decode("utf-8")
    )
    try:
        db.session.add(me)
        db.session.commit()
        print("You've been added")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {e}")
        


def clear_machines():
    machines = db.session.query(Machine).all()
    try:
        for machine in machines:
            db.session.delete(machine)
        db.session.commit()
        print("Machines deleted")
    except Exception as e:
        print(f"[ERROR]: {e}")
        

def clear_wo():
    work_orders = db.session.query(WorkOrder).all()
    try:
        for wo in work_orders:
            db.session.delete(wo)
        db.session.commit()
        print("Work orders deleted")
    except Exception as e:
        print(f"[ERROR]: {e}")
        

def clear_woe():
    work_orders = db.session.query(WorkOrderEvent).all()
    try:
        for wo in work_orders:
            db.session.delete(wo)
        db.session.commit()
        print("Work order events deleted")
    except Exception as e:
        print(f"[ERROR]: {e}")
        
        
def clear_notes():
    work_orders = db.session.query(MachineNote).all()
    try:
        for wo in work_orders:
            db.session.delete(wo)
        db.session.commit()
        print("Work orders deleted")
    except Exception as e:
        print(f"[ERROR]: {e}")
        

def clear():
    clear_notes()
    clear_woe()
    clear_wo()
    clear_machines()
    print("DB Emptied")
    

def pheonix():
    scorched_earth()
    load_me()