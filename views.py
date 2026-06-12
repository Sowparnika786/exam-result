from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course
from .models import Enrollment
from .models import Submission


def submit(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        pk=enrollment_id
    )

    selected_choices = []

    for key in request.POST:
        if key.startswith('choice'):
            selected_choices.append(int(request.POST[key]))

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    submission.choices.set(selected_choices)
    submission.save()

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            args=(enrollment.id, submission.id)
        )
    )


def show_exam_result(request, enrollment_id, submission_id):
    enrollment = get_object_or_404(
        Enrollment,
        pk=enrollment_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    context = {
        'enrollment': enrollment,
        'submission': submission,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
