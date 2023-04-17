from django.shortcuts import render
from .models import Course
from django.views import generic

class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Course.objects.all()

class CourseDetailView(generic.DeleteView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()