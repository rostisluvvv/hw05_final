from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': _('Text of post'),
            'group': _('Group'),
            'image': _('Image of post')
        }
        help_texts = {
            'text': _('Enter the text of the post'),
            'group': _('Select a group'),
            'image': _('Attach image of post'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': _('Comment to the post'),

        }
        help_texts = {
            'text': _('Enter a comment to the post'),

        }
