from light_string_manager import LightStringManager

def main():
    """
    Main function to initialize the LightStringManager, turn on all lights,
    run the converging effect, and handle graceful shutdown.
    """
    manager = LightStringManager()
    manager.turn_on_all()

    # Index of the light string where the effects should converge (0-based index)
    target_index = 4  # Change this to the desired target index

    try:
        # Run the converging effect for a specified duration and frames per second
        manager.run_converging_effect(target_index=target_index, duration=10, fps=30)
    except KeyboardInterrupt:
        print("Interrupted by user. Turning off all lights.")
    finally:
        manager.turn_off_all()

if __name__ == "__main__":
    main()