import requests

class GameStats():
    def __init__(self):
        self.abbreviation = None
        self.subscribers = None
        self.url = None

class GBGame():
    def __init__(self):
        self.name = None
        self.id = None
        self.stats = GameStats()
        self.type = 'Game'

class Date():
    def __init__(self):
        self.date:int = None # Unix

class FridayNightFunkin(GBGame):
    def __init__(self):
        super().__init__()
        self.name = 'Friday Night Funkin\''
        self.id:int = 8694

class SubmissionStats():
    def __init__(self):
        self.likes:int = None
        self.downloads:int = None
        self.comments:int = None
        self.subscribers:int = None
        self.viewCount:int = None

class SubmissionBody():
    def __init__(self):
        self.name = None 
        self.shortDescription = None
        self.text = None
        self.feedbackInstructions = None

class Category():
    def __init__(self):
        #self.game = FridayNightFunkin()
        self.name = None
        self.id = None
        self.icon = None

class User():
    def __init__(self):
        self.id:int = None
        self.username:str = None
        self.profileUrl:str = None

class Avatars():
    def __init__(self):
        self.standardDefinition = None
        self.highDefinition = None

class Css():
    def __init__(self):
        self.subjectShaper = None
        self.cooltip = None

class Titles():
    def __init__(self):
        self.online = None
        self.offline = None

class Medals():
    def __init__(self):
        self.rare = []
        self.normal = []

class Submitter(User):
    def __init__(self):
        super().__init__()

        self.joinDate = Date()
        self.points:int = None
        self.rankGlobal:int = None
        self.avatars = Avatars()

        self.cssCode = Css()
        self.titles = Titles()

        self.buddies:int = None
        self.medals = Medals()

        self.hasRipe = None
        self.isOnline = None

        self.honoraryTitle = None
        self.userTitle = None

        self.upic = None
        self.sig = None

        self.subscribers:int = None

class FileList():
    def __init__(self):
        self.tree = {}
        self.raw = []

class File():
    def __init__(self):
        self.url = None
        self.isExecutable = None
        self.id = None
        self.description = None
        self.downloadsTotal:int = None
        self.size = None
        self.name = None
        self.checksum = None
        self.date = Date()
        self.fileTree = FileList()

class FileSources():
    def __init__(self):
        self.alternate = []
        self.normal = []

class CreditedUser(User):
    def __init__(self):
        super().__init__()

        self.role = None
        self.externalSourceProfileUrl:str = None
        self.upic = None

class CreditGroup():
    def __init__(self):
        self.name = None
        self.authors = []

class Credits():
    def __init__(self):
        self.groups = []

class EmbedImages():
    def __init__(self):
        self.variations = []
        self.preferred = None
        self.baseUrl = None

class Video():
    def __init__(self):
        self.url = None

class EmbedVideos():
    def __init__(self):
        self.list = []

class ImageSize():
    def __init__(self):
        self.width = None
        self.height = None

class PreviewImage():
    def __init__(self):
        self.size = ImageSize()
        self.file = None
        self.baseUrl = None

class PreviewImages():
    def __init__(self):
        self.list = []

class FeaturedRecord():
    def __init__(self):
        self.everFeatured = None
        self.todaysPick = None
        self.bestOfYesterday = None
        self.bestOfTheBanana = None

class Submission:
    def __init__(self):
        self.game = GBGame()
        self.type = SubmissionType()
        self.id:int = None
        self.body = SubmissionBody()
        self.stats = SubmissionStats()
        self.uploaded = Date()
        self.modified = Date()
        self.updated = Date()
        self.uploader = Submitter()
        self.isUploaderCreator = None
        self.fileSources = FileSources()
        self.credits = Credits()
        self.embedImages = EmbedImages()
        self.videos = EmbedVideos()
        self.images = PreviewImages()
        self.category = Category()
        self.version = None
        self.url = None
        self.featuredStatus = FeaturedRecord()

        self.data = {}

    def populate(self, apiReference):
        self.data = apiReference
        
        match apiReference.get('_sModelName', None):
            case 'Mod':
                self.type = Mod()
            case 'Tool':
                self.type = Tool()
            case 'Script':
                self.type = Script()
            case _:
                self.type.path = apiReference.get('_sModelName', None)
                
        self.featuredStatus.everFeatured = apiReference.get('_bWasFeatured', None)
        self.featuredStatus.bestOfTheBanana = True if apiReference.get('_aFeaturings', {}).get('3day', None) else None
        self.featuredStatus.bestOfYesterday = True if apiReference.get('_aFeaturings', {}).get('yesterday', None) else None
        self.featuredStatus.todaysPick = True if apiReference.get('_aFeaturings', {}).get('today', None) else None

        self.uploaded.date = apiReference.get('_tsDateAdded', None)
        self.modified.date = apiReference.get('_tsDateModified', None)
        self.updated.date = apiReference.get('_tsDateUpdated', None)
        self.version = apiReference.get('_sVersion', None)
        self.url = apiReference.get('_sProfileUrl', None)
        self.id = apiReference.get('_idRow', None)
        self.body.name = apiReference.get('_sName', None)
        self.body.shortDescription = apiReference.get('_sDescription', None)
        self.body.feedbackInstructions = apiReference.get('_sFeedbackInstructions', None)
        self.body.text = apiReference.get('_sText', None)
        self.stats.comments = apiReference.get('_nPostCount', None)
        self.stats.downloads = apiReference.get('_nDownloadCount', None)
        self.stats.likes = apiReference.get('_nLikeCount', None)
        self.stats.viewCount = apiReference.get('_nViewCount', None)
        self.stats.subscribers = apiReference.get('_nThanksCount', None)
        self.isUploaderCreator = apiReference.get('_bCreatedBySubmitter', None)

        _aSubmitter = apiReference.get('_aSubmitter', None)
        if _aSubmitter:
            self.uploader.avatars.standardDefinition = _aSubmitter.get('_sAvatarUrl', None)
            self.uploader.avatars.highDefinition = _aSubmitter.get('_sHdAvatarUrl', None)
            self.uploader.buddies = _aSubmitter.get('_nBuddyCount', None)
            self.uploader.hasRipe = _aSubmitter.get('_bHasRipe', None)
            self.uploader.honoraryTitle = _aSubmitter.get('_sHonoraryTitle', None)
            self.uploader.id = _aSubmitter.get('_idRow', None)
            self.uploader.username = _aSubmitter.get('_sName', None)
            self.uploader.userTitle = _aSubmitter.get('_sUserTitle', None)
            self.uploader.isOnline = _aSubmitter.get('_bIsOnline', None)
            self.uploader.joinDate.date = _aSubmitter.get('_tsJoinDate', None)
            self.uploader.cssCode.cooltip = _aSubmitter.get('_sCooltipCssCode', None)
            self.uploader.cssCode.subjectShaper = _aSubmitter.get('_sSubjectShaperCssCode', None)
            self.uploader.medals.normal = _aSubmitter.get('_aNormalMedals', None)
            self.uploader.medals.rare = _aSubmitter.get('_aRareMedals', None)
            self.uploader.points = _aSubmitter.get('_nPoints', None)
            self.uploader.rankGlobal = _aSubmitter.get('_nPointsRank', None)
            self.uploader.profileUrl = _aSubmitter.get('_sProfileUrl', None)
            self.uploader.sig = _aSubmitter.get('_sSigUrl', None)
            self.uploader.titles.offline = _aSubmitter.get('_sOfflineTitle', None)
            self.uploader.titles.online = _aSubmitter.get('_sOnlineTitle', None)
            self.uploader.subscribers = _aSubmitter.get('_nSubscriberCount', None)

        _aGame = apiReference.get('_aGame', None)
        if _aGame:
            self.game.id = _aGame.get('_idRow', None)
            self.game.name = _aGame.get('_sName', None)
            self.game.stats.abbreviation = _aGame.get('_sAbbreviation', None)
            self.game.stats.subscribers = _aGame.get('_nSubscriberCount', None)

        _aCategory = apiReference.get('_aCategory', None)
        if _aCategory:
            self.category.icon = _aCategory.get('_sIconUrl', None)
            self.category.id = _aCategory.get('_idRow', None)
            self.category.name = _aCategory.get('_sName', None)

        _aAlternateFileSources = apiReference.get('_aAlternateFileSources', [])
        _aFiles = apiReference.get('_aFiles', [])

        for source in _aAlternateFileSources:
            alternateFileSource = File()
            alternateFileSource.url = source.get('url', None)
            
            alternateFileSource.name = source.get('description', None)
            self.fileSources.alternate.append(alternateFileSource)

        for source in _aFiles:
            fileSource = File()
            fileSource.url = source.get('_sDownloadUrl', None)
            fileSource.name = source.get('_sFile', None)
            fileSource.id = source.get('_idRow', None)
            fileSource.description = source.get('_sDescription', None)
            fileSource.isExecutable = source.get('_bContainsExe', None)
            fileSource.size = source.get('_nFilesize', None)
            fileSource.date.date = source.get('_tsDateAdded', None)
            fileSource.downloadsTotal = source.get('_nDownloadCount', None)
            fileSource.checksum = source.get('_sMd5Checksum', None)

            responseFileTree = requests.get(f'https://gamebanana.com/apiv11/File/{fileSource.id}')
            response = responseFileTree.json()

            fileSource.fileTree.tree = response.get('_aMetadata', {}).get('_aArchiveFileTree', [])
            
            rawFileTree = requests.get(f'https://gamebanana.com/apiv11/File/{fileSource.id}/RawFileList').text().split('\n')
            fileSource.fileTree.raw = rawFileTree

            self.fileSources.normal.append(fileSource)

        _aCredits = apiReference.get('_aCredits', [])
            
        for group in _aCredits:
            creditGroup = CreditGroup()
            creditGroup.name = group.get('_sGroupName', None)

            for author in group.get('_aAuthors', []):
                creditableAuthor = CreditedUser()
                creditableAuthor.role = author.get('_sRole', None)
                creditableAuthor.id = author.get('_idRow', None)
                creditableAuthor.username = author.get('_sName', None)
                creditableAuthor.profileUrl = author.get('_sProfileUrl', None)
                creditableAuthor.externalSourceProfileUrl = author.get('_sUrl', None)
                creditableAuthor.upic = author.get('_sUpicUrl', None)

                creditGroup.authors.append(creditableAuthor)
            self.credits.groups.append(creditGroup)

        for video in apiReference.get('_aEmbeddedMedia', []):
            self.videos.list.append(video)
            
        for image in apiReference.get('_aPreviewMedia', {}).get('_aImages', []):
            imageObj = PreviewImage()
            imageObj.baseUrl = image['_sBaseUrl'] + '/' + image['_sFile']
            
            self.images.list.append(imageObj)
    
    def __str__(self):
        return str(vars(self))

class SubmissionType():
    def __init__(self):
        self.path = None

class Mod(SubmissionType):
    def __init__(self):
        super().__init__()
        self.path = 'Mod'

class Tool(SubmissionType):
    def __init__(self):
        super().__init__()
        self.path = 'Tool'

class Script(SubmissionType):
    def __init__(self):
        super().__init__()
        self.path = 'Script'
        
class Game(SubmissionType):
    def __init__(self):
        super().__init__()
        self.path = 'Game'

class APIParams():
    def __init__(self):
        self.id = None
        self.type = SubmissionType()
        
class Subfeed():
    def __init__(self):
        self.submissions:list = []
        
    def populate(self, apiReference):
        for submission in apiReference['_aRecords']:
            sub = Submission()
            sub.populate(submission)
            
            self.submissions.append(sub)

class GameBananaAPI():
    def __init__(self):
        self.apiURL = 'https://gamebanana.com/apiv11/'

    def getSubmission(self, params:APIParams):
        request = requests.get(f'{self.apiURL}/{params.type.path}/{params.id}/ProfilePage')

        content = request.json()

        submission = Submission()
        submission.populate(content)

        return submission
    
    def getSubfeed(self, game:GBGame, parameters:dict):
        request = requests.get(f'{self.apiURL}/{game.type}/{game.id}/Subfeed', params=parameters)

        content = request.json()
        
        subfeed = Subfeed()
        subfeed.populate(content)
        
        return subfeed