#include "ap_int.h"
#include "hls_stream.h"
#include "ap_axi_sdata.h"

// Ändrad bildstorlek till 32x32
#define IMAGE_HEIGHT 32
#define IMAGE_WIDTH 32
#define MAX_PIXEL 255

typedef ap_uint<8> pixel_t;
typedef ap_axiu<8,0,0,0> axis_pixel_t;

struct rgb_pixel {
    pixel_t r;
    pixel_t g;
    pixel_t b;
};

void image_converter(
    hls::stream<axis_pixel_t>& input_stream,
    hls::stream<axis_pixel_t>& output_stream,
    ap_uint<2> conversion_type) 
{
    #pragma HLS INTERFACE axis port=input_stream
    #pragma HLS INTERFACE axis port=output_stream
    #pragma HLS INTERFACE s_axilite port=conversion_type bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control

    // Buffer för 32x32 bild
    rgb_pixel pixel_buffer[IMAGE_HEIGHT][IMAGE_WIDTH];
    #pragma HLS ARRAY_PARTITION variable=pixel_buffer complete dim=2

    // Läs in 32x32 bilden
    row_loop_read: for(int i = 0; i < IMAGE_HEIGHT; i++) {
        #pragma HLS PIPELINE II=1
        col_loop_read: for(int j = 0; j < IMAGE_WIDTH; j++) {
            #pragma HLS UNROLL
            axis_pixel_t pixel_in_r = input_stream.read();
            axis_pixel_t pixel_in_g = input_stream.read();
            axis_pixel_t pixel_in_b = input_stream.read();
            
            pixel_buffer[i][j].r = pixel_in_r.data;
            pixel_buffer[i][j].g = pixel_in_g.data;
            pixel_buffer[i][j].b = pixel_in_b.data;
        }
    }

    // Bearbeta 32x32 bilden
    row_loop_process: for(int i = 0; i < IMAGE_HEIGHT; i++) {
        #pragma HLS PIPELINE II=1
        col_loop_process: for(int j = 0; j < IMAGE_WIDTH; j++) {
            #pragma HLS UNROLL
            rgb_pixel current_pixel = pixel_buffer[i][j];
            rgb_pixel output_pixel;

            switch(conversion_type) {
                case 0: // Förstärk röd kanal
                    output_pixel.r = (current_pixel.r + 50 > MAX_PIXEL) ? MAX_PIXEL : current_pixel.r + 50;
                    output_pixel.g = current_pixel.g;
                    output_pixel.b = current_pixel.b;
                    break;
                    
                case 1: // Färgnegativ
                    output_pixel.r = MAX_PIXEL - current_pixel.r;
                    output_pixel.g = MAX_PIXEL - current_pixel.g;
                    output_pixel.b = MAX_PIXEL - current_pixel.b;
                    break;
                    
                case 2: // Färgrotation
                    output_pixel.r = current_pixel.b;
                    output_pixel.g = current_pixel.r;
                    output_pixel.b = current_pixel.g;
                    break;
                    
                default: // Oförändrad
                    output_pixel = current_pixel;
                    break;
            }

            // Skriv ut bearbetad pixel
            axis_pixel_t pixel_out_r, pixel_out_g, pixel_out_b;
            
            // Röd kanal
            pixel_out_r.data = output_pixel.r;
            pixel_out_r.keep = 1;
            pixel_out_r.strb = 1;
            pixel_out_r.user = (i == 0 && j == 0) ? 1 : 0;
            pixel_out_r.last = 0;
            pixel_out_r.id = 0;
            pixel_out_r.dest = 0;
            
            // Grön kanal
            pixel_out_g.data = output_pixel.g;
            pixel_out_g.keep = 1;
            pixel_out_g.strb = 1;
            pixel_out_g.user = 0;
            pixel_out_g.last = 0;
            pixel_out_g.id = 0;
            pixel_out_g.dest = 0;
            
            // Blå kanal
            pixel_out_b.data = output_pixel.b;
            pixel_out_b.keep = 1;
            pixel_out_b.strb = 1;
            pixel_out_b.user = 0;
            pixel_out_b.last = (i == IMAGE_HEIGHT-1 && j == IMAGE_WIDTH-1) ? 1 : 0;
            pixel_out_b.id = 0;
            pixel_out_b.dest = 0;
            
            output_stream.write(pixel_out_r);
            output_stream.write(pixel_out_g);
            output_stream.write(pixel_out_b);
        }
    }
}