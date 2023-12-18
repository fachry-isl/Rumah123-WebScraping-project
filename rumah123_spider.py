import scrapy
from scrapy_playwright.page import PageMethod

import re

class Rumah123Spider(scrapy.Spider):
    name = "rumah123"
    
    def start_requests(self):
        print(f'[Info]: Starting...')
        
        # Specify the path to your text file
        file_path = 'locations.txt'

        # Read the contents of the file into a list
        with open(file_path, 'r') as file:
            location_list = [line.strip() for line in file]

        for location in location_list:
            yield scrapy.Request(f'https://www.rumah123.com/jual/cari/?location=bekasi%2C{location}&page=1',
                meta= dict(
                    playwright=True,
                    playwright_include_page = True,
                    playwright_page_coroutines = [
                        PageMethod('wait_for_selector', 'div.card-featured__content-wrapper')
                    ]
                ))
    async def parse(self, response):
        for seq, house in enumerate(response.css("div.card-featured__content-wrapper")):
            try:
                # Parsing Price
                price = house.xpath(".//div[@class='card-featured__middle-section__price']/strong//text()").get()
                
                # Parsing House attributes
                attribute_house_dict = {'bed': '', 'bath': '', 'car': ''}
                for house_attributes in house.xpath(".//div[@class='flex ui-molecules-list__divider-none--horizontal flex-align-center flex-row flex-wrap relative ui-molecules-list']"):
                    attribute_name = house_attributes.xpath('.//span//svg//use').extract()
                    attribute_counts = house_attributes.xpath(".//span[@class='attribute-text']//text()").extract()
                    
                    for idx, name in enumerate(attribute_name):
                        name_ = re.search('#rui-icon-(\w+)-small', name).group(1)
                        attribute_house_dict[name_] = attribute_counts[idx]
                
                #print(f'Item {seq+1}: Price:{price} Attributes:{attribute_house_dict}')
                
                # Parsing LT and LB
                luas_tanah_bangunan_dict = {'LT': '', 'LB': ''}
                luas_tanah = house.xpath(".//div[@class='attribute-info']").extract()
                if len(luas_tanah) == 0:
                    pass
                elif len(luas_tanah) == 1:
                    luas_tanah_bangunan_dict['LT'] = re.search("<span>(\d+)\s*m²<\/span>", luas_tanah[0]).group(1)
                elif len(luas_tanah) == 2:
                    luas_tanah_bangunan_dict['LT'] = re.search("<span>(\d+)\s*m²<\/span>", luas_tanah[0]).group(1)
                    luas_tanah_bangunan_dict['LB'] = re.search("<span>(\d+)\s*m²<\/span>", luas_tanah[1]).group(1)
                
                    
                # Property Type
                property_badge_dict = {'property_type': '', 'listing_type': 'Regular'}
                property_badge = house.xpath(".//div[@class='card-featured__middle-section__header-badge']//div").extract()
                re_pattern = '<div data-test-id="badge-depth"(?:\s+class="[^"]*")?>(.*?)<\/div>'
                
                if len(property_badge) == 0:
                    pass
                elif len(property_badge) == 1:
                    property_badge_dict['property_type'] = re.search(re_pattern, property_badge[0]).group(1)
                elif len(property_badge) == 2:
                    property_badge_dict['property_type'] = re.search(re_pattern, property_badge[0]).group(1)
                    property_badge_dict['listing_type'] = re.search(re_pattern, property_badge[1]).group(1)
                
                #print(f'Item {seq+1}: {property_badge_dict}')
                
                # User and Agency
                username = house.xpath(".//div[@class='ui-organisms-card-r123-basic__bottom-section__agent']//p[2]/text()").get().strip()
                agent_corporate = ''
                agent = house.xpath(".//div[@class='card-featured__middle-section']/img[@alt]").get()
                match = re.search('<img[^>]*alt="([^"]*)', str(agent))
                if match != None:
                    agent = match.group(1)
                    agent_corporate = agent.strip('logo').strip()
                    #print(f'{username}, {agent_corporate}')
                
                                
                # Phone number
                phone_number = house.xpath(".//span[@class='truncate ui-atomic-ellipsis']").get()
                match = re.search('(\+[0-9.]+)', str(phone_number))
                if match != None:
                    phone_number = match.group(1)
                else:
                    phone_number = ''
                #print(f'Phone number for {seq+1}: {phone_number}')
                
                # Location
                property_location = house.xpath(".//div[@class='card-featured__middle-section']/span/text()").get()
                #print(f'Location for {seq+1}: {property_location}')

                # Property Weblink
                identifier = house.xpath(".//div[@class='card-featured__middle-section']//a[@href]").get()
                re_pattern = 'href="([^"]+)'
                match = re.search(re_pattern, str(identifier))
                if match != None:
                    identifier = match.group(1)
                    link = f'https://www.rumah123.com{identifier}'
                else:
                    link = ''
                #print(f'Link for {seq+1}: {link}')
                
                # Descriptions
                descriptions = house.xpath(".//div[@class='card-featured__middle-section']/a/h2/text()").get()
                #print(f'Descriptions for {seq+1}: {descriptions}')
                
                # Parsing partial payment (cicilan)
                # cicilan = house.xpath(".//div[@class='card-featured__middle-section__price']/em//text()").get()
                # match = re.search("\b(\d+\s*Jutaan\s*per\s*bulan\b)", str(cicilan))
                # if match != None:
                #     cicilan = match.group(1)

                # print(f'Cicilan for {seq+1}: {cicilan}')
            except Exception as e:
                print(e)
                
            yield{
            'user': username,
            'phone_number': phone_number,
            'agent_corporate': agent_corporate,
            'property_location': property_location,
            'description': descriptions,
            'price': price,
            'property_type': property_badge_dict['property_type'],
            'bed': attribute_house_dict['bed'],
            'bath': attribute_house_dict['bath'],
            'garage': attribute_house_dict['car'],
            'LT': luas_tanah_bangunan_dict['LT'],
            'LB': luas_tanah_bangunan_dict['LB'],
            'listing_type': property_badge_dict['listing_type'],
            'property_url': link
        }
            
        next_page_url = response.css("li.ui-molecule-paginate__item--next > a ::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_coroutines = [
                    PageMethod('wait_for_selector', 'div.card-featured__content-wrapper')
                ],
                errback=self.errback,
            ))
            
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
  
