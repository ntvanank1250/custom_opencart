	def get_blogs_main_export(self):
		id_src = self._notice['process']['blogs']['id_src']
		limit = self._notice['setting']['blogs']
		query = {
			'type': 'select',
			'query': "SELECT * FROM _DBPRF_blog_post WHERE post_id > " + to_str(id_src) + " ORDER BY post_id ASC LIMIT " + to_str(limit),
		}
		blogs = self.select_data_connector(query, 'blogs')
		if not blogs or blogs['result'] != 'success':
			return response_error()
		return blogs

	def get_blogs_ext_export(self, blocks):
		blogs_ids = duplicate_field_value_from_list(blocks['data'], 'post_id')
		blogs_id_con = self.list_to_in_condition(blogs_ids)
		blogs_ext_queries = {
			'blog_post_description': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_blog_post_description WHERE post_id IN " + blogs_id_con
			},
			'blog_post_related': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_blog_post_related WHERE post_id IN " + blogs_id_con,

			},
			'blog_post_to_category': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_blog_post_to_category WHERE post_id IN " + blogs_id_con,

			},
			'blog_review': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_blog_review WHERE post_id IN " + blogs_id_con,

			}
		}
		blogs_ext = self.select_multiple_data_connector(blogs_ext_queries, 'blogs')
		if not blogs_ext or blogs_ext['result'] != 'success':
			return response_error()
		return blogs_ext

	def convert_blog_export(self, block, blocks_ext):
		blog_data = {
			'id': None,
			'code': '',
			'title': '',
			'store_id': '',
			'content': '',
			'short_content': '',
			'short_description': '',
			'description': '',
			'meta_title': '',
			'meta_keywords': '',
			'meta_description': '',
			'images': list(),
			'url_key': '',
			'thumb_image': {
				'label': '',
				'url': '',
				'path': '',
			},
			'categories': list(),
			'tags': '',
			'author_id': None,
			'status': True,
			'languages': dict(),
			'created_at': '',
			'updated_at': get_current_time(),
			"comment" :list()}
		blocks_ext = blocks_ext['data']
		blog_data['id'] = block['post_id']
		blog_post_description = get_row_from_list_by_field(blocks_ext['blog_post_description'],'post_id', block['post_id'])
		blog_post_to_category = get_list_from_list_by_field(blocks_ext['blog_post_to_category'],'post_id', block['post_id'])
		blog_review = get_list_from_list_by_field(blocks_ext['blog_review'],'post_id', block['post_id'])

		blog_data['title'] = blog_post_description['name']
		blog_data['store_id'] = "0"
		content = self.strip_html_tag(html.unescape(blog_post_description['description']))
		blog_data['content'] = content
		blog_data['meta_description'] = blog_post_description.get('meta_description')
		blog_data['meta_keywords'] = blog_post_description.get('meta_keyword')
		blog_data['tags']= blog_post_description.get('tag')

		blog_data['categories'] = list()
		for blog_category in blog_post_to_category:

			cate_blog = {'id':blog_category['category_id'],
						'code':blog_category['category_id'],
						'name':''}
			blog_data['categories'].append(cate_blog)
		
		blog_post_to_category[0].get('category_id')
		blog_data['thumb_image']['url'] =  self._notice['src']['cart_url'] + "/" + self._notice['src']['config']['image']
		blog_data['thumb_image']['path'] = block['image']
		blog_data['author_id'] = block['author_id']
		blog_data['created_at'] = block['date_added']
		blog_data['updated_at'] = block['date_modified']
		for review in blog_review:
			review_blog = dict()
			review_blog['comment'] = review.get('text')
			review_blog['user'] = review.get('author')
			review_blog['id'] = review.get('review_id')
			blog_data['comment'].append(review_blog)
		return response_success(blog_data)

	def get_blog_id_import(self, convert, block, blocks_ext):
		return block['post_id']
