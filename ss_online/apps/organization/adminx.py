import xadmin
from import_export import resources
from .models import CourseOrg, Citys, Teachers
# Register your models here.

class ProductInfoResource(resources.ModelResource):

    class Meta:
        model = Citys
        skip_unchanged = True
        # 导入数据时，如果该条数据未修改过，则会忽略
        report_skipped = True
        # 在导入预览页面中显示跳过的记录
        import_id_fields = ('id',)
        # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
        fields = (
            'id',
            'name',
            'desc',
        )
        # 白名单
        exclude = (
            'add_time',
        )
        # 黑名单

class CityAdmin(object):
    # 列表页显示字段
    list_display = ['id', 'name', 'desc']
    # 支持搜索的字段
    search_fields = ['id', 'name', 'desc']
    # 过滤筛选的字段
    list_filter = ['id', 'name', 'desc', 'add_time']
    # 列表字段支持编辑
    list_editable = ['name', 'desc']
    # 分页
    list_per_page = 10
    # 配置模型图标
    model_icon = 'fa fa-laptop'

    # 配置导出导入功能
    import_export_args = {
        'import_resource_class': ProductInfoResource,
        'export_resource_class': ProductInfoResource,
    }

class TeacherAdmin(object):
    # 列表页显示字段
    list_display = ['org', 'name', 'age', 'work_year', 'work_company', 'work_position']
    # 支持搜索的字段
    search_fields = ['org', 'name', 'work_year']
    # 过滤筛选的字段
    list_filter = ['work_year', 'work_position']
    # 列表字段支持编辑
    list_editable = ['name', 'age']
    # 分页
    list_per_page = 10

class CourseOrgAdmin(object):
    # 列表页显示字段
    list_display = ['name', 'tag', 'categroy', 'course_num', 'city']
    # 支持搜索的字段
    search_fields = ['name', 'tag', 'city']
    # 过滤筛选的字段
    list_filter = ['name', 'city']
    # 列表字段支持编辑
    list_editable = ['name', 'city']
    # 分页
    list_per_page = 10

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = '明珠教育后台管理系统'
    site_footer = '明珠教育网'
    #  修改模块展示信息的样式
    menu_style = 'accordion'
    # 左侧菜单收缩功能
    apps_icons = {
        "product": "fa fa-music",
    }
    # 配置应用图标，即一级菜单图标
    # global_models_icon = {
    #     ProductInfo: "fa fa-film",
    # }

# 修改xadmin后台的主题
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
# 修改xadmin后台的相关展示信息
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(Citys, CityAdmin)
xadmin.site.register(Teachers, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)