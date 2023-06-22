from cms import CMS

class Application:
    def main(self):
        cms = CMS()
        cms.createUser("Peter", "Muster", "peter.muster@gmail.com", "0123456789")
        cms.createUser("John", "Doe", 'john.doe@example.com', "1234567890")
        cms.uploadContent("john.doe@example.com", "Monke XD", "Photo", "just monkey", "../data/image.jpg")
        cms.uploadContent("john.doe@example.com", "Testdata 1", "Photo 1", "just photo", "../data/image1.jpeg")
        cms.uploadContent("peter.muster@gmail.com", "Testdata 2", "Photo 2", "just photo 2", "../data/image2.jpg")
        cms.uploadContent("peter.muster@gmail.com", "Testdata 3", "Photo 3", "just photo 3", "../data/image3.jpg") 
        cms.copyContent("john.doe@example.com", "peter.muster@gmail.com", "Monke XD")
        cms.deleteContent(3, "peter.muster@gmail.com")
        cms.deleteUser("john.doe@example.com")

if __name__ == "__main__":
    app = Application()
    app.main()
