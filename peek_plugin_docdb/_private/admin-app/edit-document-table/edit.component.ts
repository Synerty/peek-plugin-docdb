import {Component, OnInit} from "@angular/core";
import {
    extend,
    VortexService,
    ComponentLifecycleEventEmitter,
    TupleLoader
} from "@synerty/vortexjs";
import {DocumentTuple,
    docDbFilt
} from "@peek/peek_plugin_docdb/_private";


@Component({
    selector: 'pl-docdb-edit-document',
    templateUrl: './edit.component.html'
})
export class EditDocumentComponent extends ComponentLifecycleEventEmitter {
    // This must match the dict defined in the admin_backend handler
    private readonly filt = {
        "key": "admin.Edit.DocumentTuple"
    };

    items: DocumentTuple[] = [];
    itemsToDelete: DocumentTuple[] = [];

    loader: TupleLoader;

    constructor(vortexService: VortexService) {
        super();

        this.loader = vortexService.createTupleLoader(this,
            () => {
                let filt = extend({}, this.filt, docDbFilt);
                // If we wanted to filter the data we get, we could add this
                // filt["lookupName"] = 'lookupType';
                return filt;
            });

        this.loader.observable
            .subscribe((tuples:DocumentTuple[]) => {
                this.items = tuples;
                this.itemsToDelete = [];
            });
    }

    addRow() {
        let t = new DocumentTuple();
        // Add any values needed for this list here, EG, for a lookup list you might add:
        // t.lookupName = this.lookupName;
        this.items.push(t);
    }

    removeRow(item) {
        if (item.id != null)
            this.itemsToDelete.push(item);

        let index: number = this.items.indexOf(item);
        if (index !== -1) {
            this.items.splice(index, 1);
        }
    }

    save() {
        let itemsToDelete = this.itemsToDelete;

        this.loader.save(this.items)
            .then(() => {
                if (itemsToDelete.length != 0) {
                    return this.loader.del(itemsToDelete);
                }
            });
    }

}