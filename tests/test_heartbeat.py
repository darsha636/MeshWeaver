import asyncio
from meshweaver.heartbeat import HeartbeatMonitor

async def main():
    monitor = HeartbeatMonitor("NODE1", timeout=5)

    monitor.add_peer("NODE2")

    print("Initial status:")
    print("NODE2 active:", monitor.is_active("NODE2"))

    monitor.receive_heartbeat("NODE2")

    print("\nHeartbeat received from NODE2")
    print("NODE2 active:", monitor.is_active("NODE2"))

    checker = asyncio.create_task(
        monitor.check_heartbeats()
    )

    print("\nWaiting for NODE2 heartbeat timeout...")

    await asyncio.sleep(7)

    print("\nAfter timeout:")
    print("NODE2 active:", monitor.is_active("NODE2"))

    # Test recovery
    print("\nSending heartbeat again...")
    monitor.receive_heartbeat("NODE2")

    print("NODE2 active:", monitor.is_active("NODE2"))

    checker.cancel()


if __name__ == "__main__":
    asyncio.run(main())
