from fastapi import APIRouter
from src.endpoints import (
    cancel_product_order, cancel_productorder_statechange_event,
    catalog_events_subscription, catalog_notification, charge,
    charge_notification, cross_connect_move, delete_attachment,
    events_subscription, get_auth_token, get_orders_list, health_check,
    modify_productorderItem_requested_deliverydate_notification,
    modify_request_deliverydate, order_details, performance_profile,
    performance_report, performanceprofile_notification,
    performancereport_notification, product_order,
    product_ordering_notification, upload_attachment, category, catalog_product_specification, 
    workorder, catalog_productoffering, appointment, 
    product_offering_qualification_events_subscription, product_offering_qualification_notification, 
    product_offering_qualification, workorder_event_subscription, appointment_events_subscription,appointment_notification, 
    appointment_searchtimeslot, fetch_order_status, appointment_appointment_operations ,
    geographicaddressmanagement_geographicaddress ,
    geographicsitemanagement_geographicsite, workorder_notification , trouble_ticket,performance_monitoring_events_subscription, trouble_ticket_events_subscription, customer_bill_management_customer_bill, performance_job,
    troubleticket_notification,trouble_ticket_operations,customer_bill_notification_listeners,
    customer_bill_management_events_subscription, quote_management_events_subscription)

router = APIRouter()

router.include_router(get_auth_token.router)
router.include_router(health_check.router)
router.include_router(performance_profile.router)
router.include_router(performance_report.router)
router.include_router(product_order.router)
router.include_router(product_ordering_notification.router)
router.include_router(performanceprofile_notification.router)
router.include_router(performancereport_notification.router)
router.include_router(cancel_product_order.router)
router.include_router(events_subscription.router)
router.include_router(charge_notification.router)
router.include_router(modify_request_deliverydate.router)
router.include_router(charge.router)
router.include_router(modify_productorderItem_requested_deliverydate_notification.router)
router.include_router(cancel_productorder_statechange_event.router)
router.include_router(cross_connect_move.router)
router.include_router(upload_attachment.router)
router.include_router(delete_attachment.router)
router.include_router(order_details.router)
router.include_router(catalog_notification.router)
router.include_router(catalog_events_subscription.router)
router.include_router(get_orders_list.router)
router.include_router(catalog_productoffering.router)
router.include_router(category.router)
router.include_router(workorder.router)
router.include_router(catalog_product_specification.router)
router.include_router(workorder_event_subscription.router)
router.include_router(appointment.router)
router.include_router(product_offering_qualification_events_subscription.router)
router.include_router(product_offering_qualification_notification.router)
router.include_router(product_offering_qualification.router)
router.include_router(appointment_events_subscription.router)
router.include_router(appointment_searchtimeslot.router)
router.include_router(fetch_order_status.router)
router.include_router(appointment_appointment_operations.router)
router.include_router(appointment_notification.router)
router.include_router(geographicaddressmanagement_geographicaddress.router)
router.include_router(geographicsitemanagement_geographicsite.router)
router.include_router(workorder_notification.router)
router.include_router(performance_job.router)
router.include_router(trouble_ticket.router)
router.include_router(performance_monitoring_events_subscription.router)
router.include_router(customer_bill_management_customer_bill.router)
router.include_router(trouble_ticket_events_subscription.router)
router.include_router(customer_bill_management_events_subscription.router)
router.include_router(troubleticket_notification.router)
router.include_router(trouble_ticket_operations.router)
router.include_router(customer_bill_notification_listeners.router)
router.include_router(quote_management_events_subscription.router)