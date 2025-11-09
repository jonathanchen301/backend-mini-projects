from app.models.sample import SampleItem

memory = [
    SampleItem(item_id=1, name="Item 1", description="Description 1"),
    SampleItem(item_id=2, name="Item 2", description="Description 2"),
    SampleItem(item_id=3, name="Item 3", description="Description 3"),
]

def get_sample_items() -> list[SampleItem]:
    return memory

def get_sample_item(item_id: int) -> SampleItem | None:
    for item in memory:
        if item.item_id == item_id:
            return item
    return None