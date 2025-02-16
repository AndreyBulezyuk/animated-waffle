import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
from component.models import Component
from inventory_level.models import InventoryLevel, InventoryLevelMeasurement
from django.contrib.auth.models import User
from django.db.models.signals import post_save

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for Components, InventoryLevels, and InventoryLevelMeasurements"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Generating fake data..."))

        # ✅ Ensure or create a fixed superuser
        admin_username = "admin"
        admin_password = "admin"
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email="admin@example.com",
                password=admin_password,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Created superuser: {admin_username} / {admin_password}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠️ Superuser '{admin_username}' already exists.")
            )

        # ✅ Create 50 Components
        components = [
            Component(identifier=fake.unique.uuid4()[:8], description=fake.sentence())
            for _ in range(50)
        ]
        Component.objects.bulk_create(components)
        self.stdout.write(self.style.SUCCESS("✅ Created 50 Components"))

        # ✅ Fetch created components
        components = list(Component.objects.all())

        # ✅ Create 2 Inventory Levels per Component
        inventory_levels = []
        for component in components:
            for _ in range(2):
                inventory_levels.append(
                    InventoryLevel(
                        component=component,
                        name=fake.word(),
                        metadata={
                            "sensor_type": fake.random_element(
                                ["Temperature", "Pressure", "Humidity"]
                            )
                        },
                    )
                )

        InventoryLevel.objects.bulk_create(inventory_levels)
        self.stdout.write(
            self.style.SUCCESS("✅ Created 100 Inventory Levels (2 per Component)")
        )

        # ✅ Fetch created Inventory Levels
        inventory_levels = list(InventoryLevel.objects.all())

        # ✅ Create 5 Inventory Level Measurements per Inventory Level
        measurements = []
        for inventory_level in inventory_levels:
            for _ in range(5):
                measurements.append(
                    InventoryLevelMeasurement(
                        inventory_level=inventory_level,
                        level=Decimal(
                            random.uniform(10.0, 100.0)
                        ),  # Random measurement between 10-100
                        timestamp=fake.date_time_this_year(),
                        metadata={"location": fake.city()},
                    )
                )

        InventoryLevelMeasurement.objects.bulk_create(measurements)
        self.stdout.write(
            self.style.SUCCESS(
                "✅ Created 500 Inventory Level Measurements (5 per Inventory Level)"
            )
        )
        # ✅ Trigger post_save manually for all newly created InventoryLevelMeasurements
        for measurement in InventoryLevelMeasurement.objects.all():
            post_save.send(
                sender=InventoryLevelMeasurement, instance=measurement, created=True
            )
        self.stdout.write(self.style.SUCCESS("✅ Manually triggered post_save signals"))

        self.stdout.write(self.style.SUCCESS("🎉 Fake data generation complete!"))
