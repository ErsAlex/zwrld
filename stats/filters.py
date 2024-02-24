from products.models import SoldItem

def sold_item_filter(sold_items: list[SoldItem]):
    item_quantity_dict = {}
    total_sell_price_dict = {}
    total_div_price_dict = {}
    item_article_dict = {}
    item_category_data_dict = {}
    sell_type_dict = {}
    for item in sold_items:
        sell_type_dict[item.item_category.ItemCategory_id] = item.sold_by_weight
    for item in sold_items:
        total_sell_price_dict[item.item_category.ItemCategory_id] = total_sell_price_dict.get(item.item_category.ItemCategory_id, 0) + item.price
        if sell_type_dict[item.item_category.ItemCategory_id] == True:
             total_div_price_dict[item.item_category.ItemCategory_id] = item.supply_price
        else:
            total_div_price_dict[item.item_category.ItemCategory_id] = total_div_price_dict.get(item.item_category.ItemCategory_id, 0) + item.supply_price
        item_quantity_dict[item.item_category.ItemCategory_id] = item_quantity_dict.get(item.item_category.ItemCategory_id, 0) + 1
        item_article_dict[item.item_category.ItemCategory_id] = item.item_category.article
        item_category_data_dict[item.item_category.ItemCategory_id] = item.item_category
    items_list = []
    for key in item_category_data_dict:
        category_data_dict = {}
        category_data_dict['item_category'] = item_category_data_dict[key]
        category_data_dict['article'] = item_article_dict[key]
        category_data_dict['quantity'] = item_quantity_dict[key]
        category_data_dict['total_div_price'] = total_div_price_dict[key]
        category_data_dict['total_sell_price'] = total_sell_price_dict[key]
        if sell_type_dict[key] == True:
            category_data_dict['average_div_price'] = '-'
            category_data_dict['sell_type'] = 'На развес'
        else:
            category_data_dict['average_div_price'] = round(total_div_price_dict[key] / item_quantity_dict[key], 2)
            category_data_dict['sell_type'] = 'Штучный'
        category_data_dict['average_sell_price'] = round(total_sell_price_dict[key] / item_quantity_dict[key], 2)
        items_list.append(category_data_dict)
    return items_list
            
def sold_item_category_filter(sold_items: list[SoldItem]):
    item_quantity_dict = {}
    total_sell_price_dict = {}
    total_div_price_dict = {}
    item_article_dict = {}
    item_brand_dict = {}
    item_weight_dict = {}
    item_category_data_dict = {}
    item_dry_type_dict = {}
    sell_type_dict = {}
    for item in sold_items:
        sell_type_dict[item.item_category.ItemCategory_id] = item.sold_by_weight
    
    for item in sold_items:
        total_sell_price_dict[item.item_category.ItemCategory_id] = total_sell_price_dict.get(item.item_category.ItemCategory_id, 0) + item.price
        if sell_type_dict[item.item_category.ItemCategory_id] == True:
             total_div_price_dict[item.item_category.ItemCategory_id] = item.supply_price
        else:
            total_div_price_dict[item.item_category.ItemCategory_id] = total_div_price_dict.get(item.item_category.ItemCategory_id, 0) + item.supply_price
        item_quantity_dict[item.item_category.ItemCategory_id] = item_quantity_dict.get(item.item_category.ItemCategory_id, 0) + 1
        item_article_dict[item.item_category.ItemCategory_id] = item.item_category.article
        item_category_data_dict[item.item_category.ItemCategory_id] = item.item_category.description
        item_brand_dict[item.item_category.ItemCategory_id] = item.item_category.brand
        item_weight_dict[item.item_category.ItemCategory_id] = item.item_category.weight
        item_dry_type_dict[item.item_category.ItemCategory_id] = item.item_category.is_dry
    total_items = len(sold_items)
    items_list = []
    for key in item_category_data_dict:
        category_data_dict = {}
        category_data_dict['description'] = item_category_data_dict[key]
        category_data_dict['article'] = item_article_dict[key]
        category_data_dict['quantity'] = item_quantity_dict[key]
        category_data_dict['total_div_price'] = total_div_price_dict[key]
        category_data_dict['total_sell_price'] = total_sell_price_dict[key]
        category_data_dict['brand'] = item_brand_dict[key]
        category_data_dict['weight'] = item_weight_dict[key]
        category_data_dict['dry_type'] = item_dry_type_dict[key]
        category_data_dict['sales_part'] = round((item_quantity_dict[key] / total_items) * 100, 2)
        if sell_type_dict[key] == True:
            category_data_dict['sell_type'] = 'На развес'
        else:
            category_data_dict['sell_type'] = 'Штучный'
        items_list.append(category_data_dict)
    return items_list