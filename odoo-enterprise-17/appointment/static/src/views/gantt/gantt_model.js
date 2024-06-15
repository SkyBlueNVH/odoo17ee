/** @odoo-module **/

import { Domain } from "@web/core/domain";
import { GanttModel } from "@web_gantt/gantt_model";

export class AppointmentBookingGanttModel extends GanttModel {
    /**
     * @override
     */
    load(searchParams) {
        // add some context keys to the search
        return super.load({
            ...searchParams,
            context: { ...searchParams.context, appointment_booking_gantt_show_all_resources: true }
        });
    }

    /**
     * @override
     */
    _getDomain(metaData) {
        const domainList = super._getDomain(metaData);
        const ganttDomain = this.searchParams.context.appointment_booking_gantt_domain;
        if (ganttDomain) {
            return Domain.and([domainList, ganttDomain]).toList();
        }
        return domainList;
    }
}
