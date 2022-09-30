 item_name_descriptions = ''
      order_id = self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code'])

      for item in convert['items']:
          item_name = item['product']['name'].replace("<br/>"," ")
          item_qty = item['qty']
          item_name_descriptions = item_name_descriptions + item_name + " x " + item_qty + "\n"

      self.log(item_name_descriptions,'item_name_dess')
      transaction_data = {
          "customer_id": self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['customer']['id']),
          "order_id": order_id,
          'description' : item_name_descriptions,
          'amount' : convert['total']['amount'],
          'date_added' : convert['created_at'],
      }
      self.import_data_connector(self.create_insert_query_connector('customer_transaction',transaction_data), 'insert_transaction')

