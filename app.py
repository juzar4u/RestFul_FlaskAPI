from flask import Flask, request
from flask_restful import Resource, Api
import flask_sqlalchemy
import flask

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://akhbaar24user:danat123$@172.16.3.97/Akhbaar24"
db = flask_sqlalchemy.SQLAlchemy(app)

@app.route("/")
def index():
    return flask.render_template('publicweb/index.html')

class Articles(Resource):
    def get(self, articleId):

        sql = '''select a.ArticleID,a.Title, a.Summary,a.Body, a.Source,
        a.ImageUrl, a.ImageThumbnailUrl, a.ImageTitle, a.CommentCount,
        a.ViewCount,a.IsPublished,a.IsDeleted,a.CreatedOn,
        a.UpdatedOn,a.PublishedOn,a.ShortUrl,a.SourceImage
        from articles a where ArticleID ={articleId}'''.format(articleId=articleId)
        cursor = db.engine.execute(sql)
        result = {'main_data': [
            dict(ArticleID=r[0], Title=r[1], Summary=r[2], Body=r[3], Source=r[4], ImageUrl=r[5],
                 ImageThumbnailUrl=r[6], ImageTitle=r[7], CommentCount=r[8], ViewCount=r[9], IsPublished=r[10],
                 IsDeleted=r[11], ShortUrl=r[15], SourceImage=r[16])
            for r in cursor.fetchall()]}
        return result

class Categories(Resource):
    def get(self):
        # sql = 'select count(*) from ArticleCategories where CategoryID ={catId}'.format(catId=1)
        sql = '''select c.CategoryID,c.Name,
        (select count(*) from ArticleCategories where CategoryID = c.CategoryID) as ArticleCount,
        c.DefaultCategoryImage,c.DisplayNameForMobileApp,c.IsVisibleInMobileApp from Categories c'''
        cursor = db.engine.execute(sql)
        result = {'main_data': [
            dict(CategoryID=r[0], Name=r[1], ArticleCount=r[2],
                 DefaultCategoryImage='http://a24qa.argaamnews.com/Content/CategoryImages/{text}'.format(text=r[3]),
                 DisplayNameForMobileApp=r[4], IsVisibleInMobileApp=r[5])
            for r in cursor.fetchall()]}
        return result

class CategoriesByID(Resource):
    def get(self, categoryId):
        # sql = 'select count(*) from ArticleCategories where CategoryID ={catId}'.format(catId=1)
        sql = '''select c.CategoryID,c.Name,
        (select count(*) from ArticleCategories where CategoryID = c.CategoryID) as ArticleCount,
        c.DefaultCategoryImage,c.DisplayNameForMobileApp,c.IsVisibleInMobileApp from Categories c
        where c.categoryid = {catId}'''.format(catId=categoryId)
        cursor = db.engine.execute(sql)
        result = {'main_data': [
            dict(CategoryID=r[0], Name=r[1], ArticleCount=r[2],
                 DefaultCategoryImage='http://a24webapi.argaamnews.com/Content/CategoryImages/{text}'.format(text=r[3]),
                 DisplayNameForMobileApp=r[4], IsVisibleInMobileApp=r[5])
            for r in cursor.fetchall()]}
        return result

api.add_resource(Articles, '/api/articles/<articleId>')
api.add_resource(Categories, '/api/Categories')
api.add_resource(CategoriesByID, '/api/Categories/<categoryId>')



if __name__ == '__main__':
    app.run(debug=True)