from rollback_manager import RollbackManger

if __name__=="__main__":
    repo_path="." #current repo
    manager=RollbackManger(repo_path)

    print("Current commit:",manager.get_last_commit())

    confirm =input("Do you want to rollback to the previous commit? (Yes/No):").strip().lower()
    if confirm =="Yes":
        if manager.rollback_to_previous_commit():
            manager.record_rollback()
            print("Rollback Completed Successfully!")
        else:
            print("Rollback failed . Check rollback.log for details")

    else:
        print("Rollback Cancelled.")
