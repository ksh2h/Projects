class paper_node:
    authors = []
    citing_papers = []
    keywords = []
    fields = []
    
    def __init__(self, venue, fields_array, title, year, author_array, citing_paper_array, keywords_array):
        self.venue = venue
        self.title = title
        self.year = year
        self.authors  = []
        self.citing_papers = []
        self.keywords = []
        self.fields = []
        
        for i in range(0, len(author_array)):
            self.authors.append( author_array[i] )
        for i in range(0, len(citing_paper_array)):
            self.citing_papers.append( citing_paper_array[i] )
        for i in range(0, len(keywords_array)):
            self.keywords.append( keywords_array[i] )
        for i in range(0, len(fields_array)):
            self.fields.append( fields_array[i] )
            
    def object_to_json(self):
        temp_object = {}
        temp_object['Title'] = self.title
        temp_object['Venue'] = self.venue
        temp_object['Field'] = self.fields
        temp_object['Year'] = self.year
        temp_object['Authors'] = self.authors
        temp_object['Citing Paper'] = self.citing_papers
        temp_object['Keywords'] = self.keywords
        return temp_object
      