from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
import graphql_jwt
from .models import Note as NoteModel
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Note(DjangoObjectType):

    class Meta:
        model = NoteModel
        # the data as node in graph
        interfaces = (graphene.relay.Node, )
        
       
class Query(graphene.ObjectType):
    note = graphene.List(Note, id=graphene.String(), title=graphene.String())
    all_notes = graphene.List(Note)
    users = graphene.List(UserType)

    def resolve_all_notes(self, info):
        """Decide which notes to return"""

        user = info.context.user

        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else: 
            return NoteModel.objects.filter(user=user)

    def resolve_note(self, info, **kwargs):
        # title = kwargs['title'] # exception if no key
        title = kwargs.get('title') # returns None of no key
        if title is not None:
            return NoteModel.objects.filter(title=title)
        return None

    def resolve_users(self, inf):
        return get_user_model().objects.all()

class CreateNote(graphene.Mutation):

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(self, info, title, content):
        user=info.context.user

        if user.is_anonymous:
            is_ok = False
            return CreateNote(ok=is_ok)
        
        else:
            new_note = NoteModel(title=title, content=content, user=user)
            is_ok = True
            new_note.save()

            return CreateNote(note=new_note, ok=is_ok)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = get_user_model() (
            username=username,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# Add a schema and attach the query
schema = graphene.Schema(query=Query, mutation=Mutation)

