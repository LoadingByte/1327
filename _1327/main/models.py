from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from _1327.documents.models import Document

MENUITEM_VIEW_PERMISSION_NAME = 'view_menuitem'


class MenuItem(models.Model):
	MAIN_MENU = 1
	FOOTER = 2
	MENU_TYPES = (
		(MAIN_MENU, _("Main Menu")),
		(FOOTER, _("Footer")),
	)
	title = models.CharField(max_length=255, unique=False, verbose_name=_("Title"))
	order = models.IntegerField(default=999)

	link = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Link"))
	document = models.ForeignKey(Document, blank=True, null=True, verbose_name=_("Document"))

	parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

	menu_type = models.IntegerField(choices=MENU_TYPES, default=MAIN_MENU)

	VIEW_PERMISSION_NAME = MENUITEM_VIEW_PERMISSION_NAME

	class Meta:
		ordering = ['order']
		permissions = (
			(MENUITEM_VIEW_PERMISSION_NAME, 'User/Group is allowed to view this menu item'),
		)

	def __str__(self):
		return self.title

	def get_url(self):
		if self.link:
			return reverse(self.link)
		elif self.document:
			return self.document.get_view_url()
		else:
			return "#"

	def can_view(self, user):
		permission_name = MENUITEM_VIEW_PERMISSION_NAME
		return user.has_perm(permission_name, self) or user.has_perm(permission_name)

	def can_edit(self, user):
		permission_name = 'change_menuitem'
		return user.has_perm(permission_name, self.parent) or user.has_perm(permission_name)

	def can_delete(self, user):
		permission_name = 'delete_menuitem'
		return user.has_perm(permission_name, self) or user.has_perm(permission_name)
