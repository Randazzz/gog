from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    extra_context = {'title': 'Спасибо за заказ!'}
    template_name = 'orders/success.html'


class CanceledTemplateView(TemplateView):
    extra_context = {'title': 'Оплата отменена!'}
    template_name = 'orders/canceled.html'


class OrderListView(ListView):
    template_name = 'orders/orders.html'
    extra_context = {'title': 'Заказы'}
    queryset = Order.objects.all()
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Заказ #{self.object.id}'
        return context


class OrderCreateView(CreateView):
    extra_context = {'title': 'Оформление заказа'}
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=settings.DOMAIN_NAME + reverse('orders:order_success'),
            cancel_url=settings.DOMAIN_NAME + reverse('orders:order_canceled'),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object']['id'])

    return HttpResponse(status=200)


def fulfill_checkout(session_id):
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )
    order_id = int(checkout_session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    # if checkout_session.payment_status != 'unpaid':
